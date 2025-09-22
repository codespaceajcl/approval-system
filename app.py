import sendEmail
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response
import os
import mysql.connector
import jwt
from datetime import datetime, timedelta

from functools import wraps


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'attachments'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['JWT_SECRET'] = 'your_jwt_secret'  # Change this in production

# MySQL connection config
db_config = {
    'host': 'localhost',
    'user': 'approval',
    'password': 'Ajcl@113A#',
    'database': 'approval_system'
}


def get_db():
    return mysql.connector.connect(**db_config)

# JWT helper functions
def generate_jwt(email, role):
    payload = {
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
        return payload
    except Exception:
        return None

# Decorator for protected routes
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token') or request.headers.get('Authorization')
        if not token:
            return redirect(url_for('signin'))
        payload = verify_jwt(token)
        if not payload:
            return redirect(url_for('signin'))
        session['email'] = payload['email']
        session['role'] = payload['role']
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        if user:
            token = generate_jwt(user['email'], user['role'])
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('jwt_token', token, httponly=True, samesite='Lax')
            return resp
        error = 'Invalid credentials'
    return render_template('signin.html', error=error)

@app.route('/dashboard')
@jwt_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    role = session['role']
    if role == 'Finance' or role == 'finance':
        cursor.execute("SELECT * FROM requests WHERE LOWER(approval_status)='approved' ORDER BY created_date DESC LIMIT 5")
    else:
        cursor.execute("SELECT * FROM requests ORDER BY created_date DESC LIMIT 5")
    requests_db = cursor.fetchall()

    # Trend data: requests per day
    cursor.execute("SELECT DATE(created_date) as date, COUNT(*) as count FROM requests GROUP BY DATE(created_date) ORDER BY date")
    trend_rows = cursor.fetchall()
    trend_data = {
        'labels': [row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date']) for row in trend_rows],
        'counts': [row['count'] for row in trend_rows]
    }

    # Department bar chart: requests by department
    if role == 'Finance' or role == 'finance':
        cursor.execute("SELECT requested_by, COUNT(*) as count FROM requests WHERE LOWER(approval_status)='approved' GROUP BY requested_by")
    else:
        cursor.execute("SELECT requested_by, COUNT(*) as count FROM requests GROUP BY requested_by")
    dept_rows = cursor.fetchall()
    dept_data = {
        'labels': [row['requested_by'] for row in dept_rows],
        'counts': [row['count'] for row in dept_rows]
    }

    cursor.close()
    db.close()
    return render_template('dashboard.html', requests=requests_db, role=role, trend_data=trend_data, dept_data=dept_data)

@app.route('/add-request', methods=['GET', 'POST'])
@jwt_required
def add_request():
    role = session['role']
    if role == 'Finance' or role == 'finance':
        return redirect(url_for('dashboard'))
    user_email = session.get('email')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    departments = []
    user_name = ''
    user_dept = ''
    if role == 'manager' or role == 'employee':
        cursor.execute("SELECT name, department FROM users WHERE email=%s", (user_email,))
        user_row = cursor.fetchone()
        user_name = user_row['name'] if user_row and user_row['name'] else user_email
        if not user_name:
            user_name = user_email
        user_dept = user_row['department'] if user_row and user_row['department'] else 'Unknown'
        if not user_dept:
            user_dept = 'Unknown'
        if user_dept:
            cursor.execute("SELECT * FROM departments WHERE name = %s", (user_dept,))
            departments = cursor.fetchall()
    elif role == 'senior_manager':
        cursor.execute("SELECT name, department FROM users WHERE email=%s", (user_email,))
        user_row = cursor.fetchone()
        user_name = user_row['name'] if user_row and user_row['name'] else user_email
        if not user_name:
            user_name = user_email
        user_dept = user_row['department'] if user_row and user_row['department'] else 'Unknown'
        if not user_dept:
            user_dept = 'Unknown'
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
    success = None
    if request.method == 'POST':
        reference_no = request.form['reference_no']
        date_of_request = request.form['date_of_request']
        requested_by = request.form['requested_by']
        request_type = request.form['request_type']
        description = request.form['description']
        quantity = request.form.get('quantity')
        estimated_cost = request.form.get('estimated_cost')
        priority_level = request.form['priority_level']
        supporting_documents = request.form['supporting_documents']
        remarks = request.form.get('remarks')
        owner = session['email']
        # Set status based on role
        if role == 'employee':
            status = 'Submitted'
        elif role == 'manager':
            status = 'Provisionally Approved'
        elif role == 'senior_manager':
            status = 'Approved'
        else:
            status = 'Submitted'
        attachment_path = None
        if supporting_documents == 'Yes' and 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                filename = f"{owner}_{file.filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                attachment_path = filepath
        import datetime
        created_by = owner
        created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor2 = db.cursor()
        cursor2.execute("INSERT INTO requests (reference_no, date_of_request, requested_by, request_type, description, quantity, estimated_cost, priority_level, supporting_documents, approval_status, owner, attachment, remarks, created_by, created_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (reference_no, date_of_request, requested_by, request_type, description, quantity, estimated_cost, priority_level, supporting_documents, status, owner, attachment_path, remarks, created_by, created_date))
        db.commit()
        cursor2.close()
        db.close()
        success = 'Request added successfully.'

        # Email notification logic
        """<div style='font-family:Segoe UI,Arial,sans-serif;background:#f8fafc;padding:32px;'>
            <div style='max-width:520px;margin:auto;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;padding:32px;'>
                <h2 style='color:#2563eb;margin-bottom:18px;'>Approval System Notification</h2>
                <p style='font-size:1.1rem;color:#334155;'>A new request has been added:</p>
                <table style='width:100%;margin:18px 0 24px 0;border-collapse:collapse;'>
                    <tr><td style='font-weight:600;padding:6px 0;'>Reference No.:</td><td>{reference_no}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Request Type:</td><td>{request_type}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Description:</td><td>{description}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Requested By:</td><td>{requested_by}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Status:</td><td>{status}</td></tr>
                </table>
                <div style='color:#64748b;font-size:0.98rem;'>This is an automated notification from the Approval System.</div>
            </div>
        </div>
        """
        subject = f"New Request Added: {reference_no}"
        body = f"""
                <div style='font-family:Segoe UI,Arial,sans-serif;background:#f8fafc;padding:32px;'>
                    <div style='max-width:520px;margin:auto;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;padding:32px;'>
                        <h2 style='color:#2563eb;margin-bottom:18px;'>Approval System Notification</h2>
                        <p style='font-size:1.1rem;color:#334155;'>A new request has been added:</p>
                        <table style='width:100%;margin:18px 0 24px 0;border-collapse:collapse;'>
                            <tr><td style='font-weight:600;padding:6px 0;'>Reference No.:</td><td>{reference_no}</td></tr>
                            <tr><td style='font-weight:600;padding:6px 0;'>Request Type:</td><td>{request_type}</td></tr>
                            <tr><td style='font-weight:600;padding:6px 0;'>Description:</td><td>{description}</td></tr>
                            <tr><td style='font-weight:600;padding:6px 0;'>Requested By:</td><td>{requested_by}</td></tr>
                            <tr><td style='font-weight:600;padding:6px 0;'>Status:</td><td>{status}</td></tr>
                        </table>
                        <div style='color:#64748b;font-size:0.98rem;'>This is an automated notification from the Approval System.</div>
                    </div>
                </div>
                """
        recipients = []
        if role == 'employee':
            # Notify department managers and employee
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT email FROM users WHERE role='manager' AND department=%s", (user_dept,))
            managers = [row['email'] for row in cursor.fetchall()]
            recipients = managers + [user_email]
            cursor.close()
            db.close()
        elif role == 'manager':
            # Notify senior manager and manager
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT email FROM users WHERE role='senior_manager' OR role='Senior Manager'")
            seniors = [row['email'] for row in cursor.fetchall()]
            recipients = seniors + [user_email]
            cursor.close()
            db.close()
        elif role == 'senior_manager':
            # Notify finance and senior manager
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT email FROM users WHERE role='finance'")
            finance = [row['email'] for row in cursor.fetchall()]
            recipients = finance + [user_email]
            cursor.close()
            db.close()
        if recipients:
            for r in recipients:
                sendEmail.sendMail(body, r, [])
        return render_template('add_request.html', role=role, departments=departments, user_name=user_name, user_dept=user_dept, success=success)
    cursor.close()
    db.close()
    return render_template('add_request.html', role=role, departments=departments, user_name=user_name, user_dept=user_dept)

@app.route('/approve/<int:req_id>')
@jwt_required
def approve(req_id):
    role = session['role']
    user_email = session.get('email')
    if role in ['manager', 'senior_manager']:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        # Update status
        cursor.execute("UPDATE requests SET approval_status='approved' WHERE id=%s AND approval_status='pending'", (req_id,))
        db.commit()
        # Fetch request details for email
        cursor.execute("SELECT * FROM requests WHERE id=%s", (req_id,))
        req = cursor.fetchone()
        subject = f"Request Approved: {req['reference_no']}"
        body = f"""
        <div style='font-family:Segoe UI,Arial,sans-serif;background:#f8fafc;padding:32px;'>
            <div style='max-width:520px;margin:auto;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;padding:32px;'>
                <h2 style='color:#2563eb;margin-bottom:18px;'>Approval System Notification</h2>
                <p style='font-size:1.1rem;color:#334155;'>A request has been approved:</p>
                <table style='width:100%;margin:18px 0 24px 0;border-collapse:collapse;'>
                    <tr><td style='font-weight:600;padding:6px 0;'>Reference No.:</td><td>{req['reference_no']}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Request Type:</td><td>{req['request_type']}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Description:</td><td>{req['description']}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Requested By:</td><td>{req['requested_by']}</td></tr>
                    <tr><td style='font-weight:600;padding:6px 0;'>Status:</td><td>Approved</td></tr>
                </table>
                <div style='color:#64748b;font-size:0.98rem;'>This is an automated notification from the Approval System.</div>
            </div>
        </div>
        """
        recipients = []
        if role == 'manager':
            # Notify senior manager(s)
            cursor.execute("SELECT email FROM users WHERE role='senior_manager' OR role='Senior Manager'")
            seniors = [row['email'] for row in cursor.fetchall()]
            recipients = seniors
        elif role == 'senior_manager':
            # Notify finance
            cursor.execute("SELECT email FROM users WHERE role='finance' OR role='Finance'")
            finance = [row['email'] for row in cursor.fetchall()]
            recipients = finance
        # Send email notifications
        else:pass
        print("role",role)
        print("recipients",recipients)
        if recipients:
            for r in recipients:
                sendEmail.sendMail(body, r, [])
        cursor.close()
        db.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('signin')))
    resp.delete_cookie('jwt_token')
    return resp

@app.route('/requests')
@jwt_required
def requests_page():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    role = session['role']
    # Normalize role for frontend logic
    if role.replace(' ', '_').lower() == 'senior_manager':
        role = 'senior_manager'
    #print("User role:", role)  # Debugging line
    if role == 'finance':
        cursor.execute("SELECT *, LOWER(approval_status) as approval_status, IFNULL(created_by, owner) AS created_by, IFNULL(created_date, date_of_request) AS created_date FROM requests WHERE LOWER(approval_status)='approved' or LOWER(approval_status)='completed'")
    else:
        cursor.execute("SELECT *, IFNULL(created_by, owner) AS created_by, IFNULL(created_date, date_of_request) AS created_date FROM requests")
    requests_db = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('requests.html', requests=requests_db, role=role)


# Add User route
@app.route('/add-user', methods=['GET', 'POST'])
@jwt_required
def add_user():
    role = session.get('role')
    if role not in ['manager', 'senior_manager', 'finance']:
        return redirect(url_for('dashboard'))
    error = None
    success = None
    db = get_db()
    cursor = db.cursor(dictionary=True)
    user_email = session.get('email')
    user_dept = None
    departments = []
    if role == 'manager':
        cursor.execute("SELECT department FROM users WHERE email=%s", (user_email,))
        user_row = cursor.fetchone()
        user_dept = user_row['department'] if user_row else None
        if user_dept:
            cursor.execute("SELECT * FROM departments WHERE name = %s", (user_dept,))
            departments = cursor.fetchall()
    elif role == 'senior_manager':
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
    elif role == 'finance':
        departments = ['Finance']

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role_new = request.form['role']
        department = request.form.get('department', None)
        # Insert new user into database
        try:
            cursor.execute("INSERT INTO users (name, email, password, role, department) VALUES (%s, %s, %s, %s, %s)",
                           (name, email, password, role_new, department))
            db.commit()
            success = 'User registered successfully.'
        except Exception as e:
            error = f'Error registering user: {str(e)}'
        # Optionally, send email notification to new user or admins here
        return render_template('add_user.html', role=role, error=error, success=success, departments=departments)
    return render_template('add_user.html', role=role, error=error, success=success, departments=departments)

def log_status_update(req_id, new_status, user_email, attachment_path=None):
    db_log = get_db()
    cursor_log = db_log.cursor()
    import datetime
    log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor_log.execute("INSERT INTO request_status_log (request_id, status, updated_by, updated_at, attachment) VALUES (%s, %s, %s, %s, %s)", (req_id, new_status, user_email, log_time, attachment_path))
    db_log.commit()
    cursor_log.close()
    db_log.close()

# Add this route to handle AJAX status updates
@app.route('/update-status', methods=['POST'])
@jwt_required
def update_status():
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        req_id = request.form.get('id')
        new_status = request.form.get('status')
        file = request.files.get('attachment')
        attachment_path = None
        if file and file.filename:
            filename = f"finance_{req_id}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            attachment_path = filepath
        if not req_id or not new_status:
            return jsonify({'success': False, 'error': 'Missing data'})
        # Validate attachment is mandatory for Completed status
        if new_status == 'Completed' and not attachment_path:
            return jsonify({'success': False, 'error': 'Attachment is required to complete this request.'})
        db = get_db()
        cursor = db.cursor()
        try:
            if attachment_path:
                cursor.execute("UPDATE requests SET approval_status=%s, financial_reference=%s WHERE id=%s", (new_status, attachment_path, req_id))
            else:
                cursor.execute("UPDATE requests SET approval_status=%s WHERE id=%s", (new_status, req_id))
            db.commit()
            log_status_update(req_id, new_status, session.get('email'), attachment_path)
            # Email notification logic after status update
            cursor.execute("SELECT * FROM requests WHERE id=%s", (req_id,))
            req = cursor.fetchone()

            subject = f"Request Status Updated: {req[6]}"
            body = f"""
            <div style='font-family:Segoe UI,Arial,sans-serif;background:#f8fafc;padding:32px;'>
                <div style='max-width:520px;margin:auto;background:#fff;border-radius:12px;box-shadow:0 4px 24px #0001;padding:32px;'>
                    <h2 style='color:#2563eb;margin-bottom:18px;'>Approval System Notification</h2>
                    <p style='font-size:1.1rem;color:#334155;'>A request status has been updated:</p>
                    <table style='width:100%;margin:18px 0 24px 0;border-collapse:collapse;'>
                        <tr><td style='font-weight:600;padding:6px 0;'>Reference No.:</td><td>{req[6]}</td></tr>
                        <tr><td style='font-weight:600;padding:6px 0;'>Request Type:</td><td>{req[9]}</td></tr>
                        <tr><td style='font-weight:600;padding:6px 0;'>Description:</td><td>{req[2]}</td></tr>
                        <tr><td style='font-weight:600;padding:6px 0;'>Requested By:</td><td>{req[8]}</td></tr>
                        <tr><td style='font-weight:600;padding:6px 0;'>New Status:</td><td>{new_status}</td></tr>
                    </table>
                    <div style='color:#64748b;font-size:0.98rem;'>This is an automated notification from the Approval System.</div>
                </div>
            </div>
            """
            recipients = []
            role = session.get('role')
            user_email = session.get('email')
            print("role", role)
            if role.lower().replace(' ', '_') == 'finance' and new_status == 'Completed':
                # Notify all senior managers with attachment
                cursor.execute("SELECT email FROM users WHERE LOWER(REPLACE(role, ' ', '_'))='senior_manager'")
                seniors = [row[0] for row in cursor.fetchall()]
                recipients = seniors
            elif role == 'manager':
                # Notify senior manager and manager
                cursor.execute("SELECT id,email FROM users WHERE role='senior_manager' OR role='Senior Manager'")
                seniors = [row[1] for row in cursor.fetchall()]
                recipients = seniors + [user_email]
            elif role == 'senior_manager' or role == 'Senior Manager':
                # Notify finance and senior manager
                cursor.execute("SELECT id,email FROM users WHERE role='finance' OR role='Finance'")
                finance = [row[1] for row in cursor.fetchall()]
                recipients = finance + [user_email]
            print("role", role)
            print("recipients", recipients)
            if recipients:
                for r in recipients:
                    docPath = [attachment_path] if attachment_path else []
                    sendEmail.sendMail(body, r, docPath)
            cursor.close()
            db.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': str(e)})
    else:
        print("Non-multipart request received")
        data = request.get_json()
        req_id = data.get('id')
        new_status = data.get('status')
        if not req_id or not new_status:
            return jsonify({'success': False, 'error': 'Missing data'})
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE requests SET approval_status=%s WHERE id=%s", (new_status, req_id))
            db.commit()
            log_status_update(req_id, new_status, session.get('email'))
            cursor.close()
            db.close()
            return jsonify({'success': True})
        except Exception as e:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'error': str(e)})

@app.route('/edit-request/<int:req_id>', methods=['GET', 'POST'])
@jwt_required
def edit_request(req_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM requests WHERE id=%s", (req_id,))
    req = cursor.fetchone()
    if not req:
        cursor.close()
        db.close()
        return "Request not found", 404
    role = session.get('role')
    # Finance cannot edit
    if role in ['finance', 'Finance']:
        cursor.close()
        db.close()
        return "Finance users cannot edit requests.", 403
    # Senior manager can edit only provisionally approved
    if role == 'senior_manager' and req['approval_status'] != 'Provisionally Approved':
        cursor.close()
        db.close()
        return "Senior manager can only edit provisionally approved requests.", 403
    # Manager/employee can edit only submitted
    if role in ['manager', 'employee'] and req['approval_status'] != 'Submitted':
        cursor.close()
        db.close()
        return "Manager/employee can only edit submitted requests.", 403
    if request.method == 'POST':
        # Update fields from form
        fields = ['reference_no', 'date_of_request', 'request_type', 'description', 'quantity', 'estimated_cost', 'priority_level', 'supporting_documents', 'remarks']
        updates = []
        values = []
        for field in fields:
            if field in request.form:
                updates.append(f"{field}=%s")
                values.append(request.form[field])
        values.append(req_id)
        if updates:
            cursor.execute(f"UPDATE requests SET {', '.join(updates)} WHERE id=%s", tuple(values))
            db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('requests_page'))
    cursor.close()
    db.close()
    return render_template('edit_request.html', req=req)

@app.route('/add-department', methods=['GET', 'POST'])
@jwt_required
def add_department():
    role = session.get('role')
    if role != 'senior_manager':
        return redirect(url_for('dashboard'))
    error = None
    success = None
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            error = 'Department name is required.'
            return render_template('add_department.html', role=role, error=error, success=success)
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO departments (name) VALUES (%s)", (name,))
            db.commit()
            cursor.close()
            db.close()
            success = 'Department added successfully.'
        except Exception as e:
            error = f'Error adding department: {str(e)}'
    return render_template('add_department.html', role=role, error=error, success=success)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
