-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 24, 2025 at 01:32 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `approval_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`id`, `name`) VALUES
(4, 'Ajcl'),
(3, 'ImmenseCode'),
(5, 'Test');

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `status` enum('pending','approved') NOT NULL,
  `owner` varchar(255) NOT NULL,
  `attachment` varchar(255) DEFAULT NULL,
  `reference_no` varchar(100) DEFAULT NULL,
  `date_of_request` date DEFAULT NULL,
  `requested_by` varchar(255) DEFAULT NULL,
  `request_type` varchar(50) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `estimated_cost` decimal(12,2) DEFAULT NULL,
  `priority_level` varchar(20) DEFAULT NULL,
  `supporting_documents` varchar(10) DEFAULT NULL,
  `approval_status` enum('Submitted','Under Review','Provisionally Approved','Provisionally Rejected','Final Review','Approved','Rejected','Completed') DEFAULT 'Submitted',
  `approved_by` varchar(255) DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `created_by` varchar(255) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `financial_reference` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`id`, `title`, `description`, `status`, `owner`, `attachment`, `reference_no`, `date_of_request`, `requested_by`, `request_type`, `quantity`, `estimated_cost`, `priority_level`, `supporting_documents`, `approval_status`, `approved_by`, `remarks`, `created_by`, `created_date`, `financial_reference`) VALUES
(1, '', '0', 'pending', 'msohaibajcl@gmail.com', 'attachments\\msohaibajcl@gmail.com_HIRING OF SERVICES FOR DIGITAL TRANSFORMATION.pdf', 'Test1', '2025-09-19', 'employee (ImmenseCode)', 'Purchase', 1, 0.00, 'High', 'Yes', 'Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-19 17:00:27', ''),
(2, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test2', '2025-09-19', 'employee (ImmenseCode)', 'Purchase', 1, 0.00, 'High', 'No', 'Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-19 18:10:35', ''),
(3, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test3', '2025-09-19', 'employee (ImmenseCode)', 'Finance', 1, 0.00, 'Medium', 'No', 'Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-19 18:16:56', ''),
(4, '', '0', 'pending', 'muhammadsohaib1267@gmail.com', NULL, 'testm1', '2025-09-20', 'manager (ImmenseCode)', 'IT', 1, 0.00, 'High', 'No', 'Approved', NULL, '0', 'muhammadsohaib1267@gmail.com', '2025-09-19 18:45:28', ''),
(5, '', '0', 'pending', 'codespaceajcl@gmail.com', NULL, 'testsm', '2025-09-19', 'seniorManager (ImmenseCode)', 'Purchase', 1, 0.00, 'High', 'No', 'Completed', NULL, '0', 'codespaceajcl@gmail.com', '2025-09-19 18:59:24', 'attachments\\finance_5_download.png'),
(6, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test4', '2025-09-19', 'employee (ImmenseCode)', 'HR', 1, 0.00, 'Low', 'No', 'Provisionally Approved', NULL, '0\r\n', 'msohaibajcl@gmail.com', '2025-09-19 19:02:50', ''),
(7, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test5', '2025-09-20', 'employee (ImmenseCode)', 'Finance', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-19 19:03:40', ''),
(8, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test6', '2025-09-19', 'employee (ImmenseCode)', 'Finance', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-19 19:04:01', ''),
(9, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test7', '2025-09-19', 'employee (ImmenseCode)', 'Purchase', 1, 0.00, 'Medium', 'No', 'Provisionally Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-19 19:04:22', ''),
(10, '', 'mmm', 'pending', 'msohaibajcl@gmail.com', NULL, 'test8', '2025-09-22', 'employee (ImmenseCode)', 'Purchase', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, '000\r\n', 'msohaibajcl@gmail.com', '2025-09-22 04:22:59', ''),
(11, '', 'aaa', 'pending', 'msohaibajcl@gmail.com', NULL, 'test9', '2025-09-22', 'employee (ImmenseCode)', 'Purchase', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-22 04:26:52', ''),
(12, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test10', '2025-09-23', 'employee (ImmenseCode)', 'Finance', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, 'bbb', 'msohaibajcl@gmail.com', '2025-09-22 04:27:21', ''),
(13, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test11', '2025-09-22', 'employee (ImmenseCode)', 'Purchase', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, 'nnn', 'msohaibajcl@gmail.com', '2025-09-22 04:33:09', ''),
(14, '', '0', 'pending', 'msohaibajcl@gmail.com', NULL, 'test12', '2025-09-22', 'employee (ImmenseCode)', 'Finance', 1, 0.00, 'High', 'No', 'Completed', NULL, '0', 'msohaibajcl@gmail.com', '2025-09-22 04:33:31', 'attachments\\finance_14_download.png'),
(15, '', '000', 'pending', 'muhammadsohaib1267@gmail.com', NULL, 'test13', '2025-09-24', 'manager (ImmenseCode)', 'IT', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, '0', 'muhammadsohaib1267@gmail.com', '2025-09-22 05:10:44', ''),
(16, '', 'testing', 'pending', 'muhammadsohaib1267@gmail.com', NULL, 'Demo1', '2025-09-22', 'manager (ImmenseCode)', 'HR', 1, 0.00, 'High', 'No', 'Provisionally Approved', NULL, 'testing', 'muhammadsohaib1267@gmail.com', '2025-09-22 11:07:30', ''),
(17, '', 'abc', 'pending', 'muhammad.abdurrehman@ajcl.net', NULL, 'Demo-Test-1', '2025-09-23', 'Demo1 (ImmenseCode)', 'Finance', 1, 0.00, 'High', 'No', 'Completed', NULL, 'abc', 'muhammad.abdurrehman@ajcl.net', '2025-09-22 11:14:02', 'attachments\\finance_17_Two way vehicle counting (1).docx'),
(18, '', 'aaa', 'pending', 'codespaceajcl@gmail.com', NULL, 'ImmenseCode-1', '2025-09-22', 'seniorManager (ImmenseCode)', 'IT', 1, 0.00, 'High', 'No', 'Completed', NULL, 'nnn', 'codespaceajcl@gmail.com', '2025-09-22 13:43:54', 'attachments\\finance_18_Two way vehicle counting (1).docx');

-- --------------------------------------------------------

--
-- Table structure for table `request_status_log`
--

CREATE TABLE `request_status_log` (
  `id` int(11) NOT NULL,
  `request_id` int(11) NOT NULL,
  `status` varchar(64) NOT NULL,
  `updated_by` varchar(128) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `attachment` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `request_status_log`
--

INSERT INTO `request_status_log` (`id`, `request_id`, `status`, `updated_by`, `updated_at`, `attachment`) VALUES
(1, 1, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-19 18:21:40', NULL),
(2, 2, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-19 18:32:32', NULL),
(3, 3, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-19 18:43:56', NULL),
(4, 4, 'Approved', 'codespaceajcl@gmail.com', '2025-09-19 18:47:44', NULL),
(5, 2, 'Approved', 'codespaceajcl@gmail.com', '2025-09-19 18:54:24', NULL),
(6, 3, 'Approved', 'codespaceajcl@gmail.com', '2025-09-19 18:57:40', NULL),
(7, 1, 'Approved', 'codespaceajcl@gmail.com', '2025-09-19 18:57:56', NULL),
(8, 6, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-19 19:10:13', NULL),
(9, 7, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:13:39', NULL),
(10, 8, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:17:07', NULL),
(11, 9, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:20:13', NULL),
(12, 10, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:23:43', NULL),
(13, 11, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:27:44', NULL),
(14, 12, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:28:33', NULL),
(15, 13, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:33:54', NULL),
(16, 14, 'Provisionally Approved', 'muhammadsohaib1267@gmail.com', '2025-09-22 04:36:09', NULL),
(17, 14, 'Approved', 'codespaceajcl@gmail.com', '2025-09-22 04:37:47', NULL),
(18, 14, 'Completed', 'sohaib.akram@ajcl.net', '2025-09-22 04:38:45', 'attachments\\finance_14_download.png'),
(19, 5, 'Completed', 'sohaib.akram@ajcl.net', '2025-09-22 04:41:43', 'attachments\\finance_5_download.png'),
(20, 14, 'Completed', 'sohaib.akram@ajcl.net', '2025-09-22 05:08:51', 'attachments\\finance_14_download.png'),
(21, 17, 'Approved', 'codespaceajcl@gmail.com', '2025-09-22 11:15:33', NULL),
(22, 17, 'Completed', 'sohaib.akram@ajcl.net', '2025-09-22 11:17:41', 'attachments\\finance_17_Two way vehicle counting (1).docx'),
(23, 18, 'Completed', 'sohaib.akram@ajcl.net', '2025-09-22 13:45:03', 'attachments\\finance_18_Two way vehicle counting (1).docx'),
(24, 17, 'Completed', 'sohaib.akram@ajcl.net', '2025-09-22 13:46:27', 'attachments\\finance_17_Two way vehicle counting (1).docx');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('employee','manager','senior_manager','finance') NOT NULL,
  `name` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `verification_token` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `role`, `name`, `department`, `is_verified`, `verification_token`) VALUES
(6, 'sohaib.akram@ajcl.net', '$2b$12$qwz8A3VFwUvtXKyTHwl.3.Dyqhtt5CyQ948QFhQFRvSAtE4/k4UbG', 'finance', 'Finance User', 'Finance', 1, NULL),
(8, 'msohaibajcl@gmail.com', '$2b$12$4pL0G0k3FC/jmVV5pNDY/upaeol1c/2ewoBfo92uYYRS1dWrjMHHG', 'employee', 'employee', 'ImmenseCode', 1, NULL),
(9, 'muhammadsohaib1267@gmail.com', '$2b$12$zz1ljorHU6X7jkhwSwh/p.cbvTCyUPDQtREaOVA6ckWEvtl8u9kbC', 'manager', 'manager', 'ImmenseCode', 1, NULL),
(10, 'codespaceajcl@gmail.com', '$2b$12$1cRJERSFIx.qGVyyW8pvFOsTRpQnL6lTYIHA8vkIJkvg8a92oW0a6', 'senior_manager', 'seniorManager', 'ImmenseCode', 1, NULL),
(11, 'test@gmail.com', '$2b$12$WV62VXJsG1FfphEYAe0w6eu4KRUGbHzWMNGyuwrCSseW17bIWEk6G', 'employee', 'test', 'ImmenseCode', 1, NULL),
(12, 'muhammad.abdurrehman@ajcl.net', '$2b$12$mKi5x6jVZiN17/XDyTF6WuhbTwUqYOxCX9hpirgScjpOLcAYvZ2qW', 'manager', 'Demo1', 'ImmenseCode', 1, NULL),
(13, 'ali.syed@ajcl.net', '$2b$12$vNC3x6DkPzL34rkiFDxU0.vkXj0SaC5yD6KhVqLSogC3pkfzid.6m', 'senior_manager', 'Ali Syed', 'ImmenseCode', 1, NULL),
(15, 'msojaibajcl@gmail.com', '$2b$12$PuY6tKzk3szrEH2.DL68s.kd8fkTKiLYTuwrzWWqJKZ08TJY59BcC', 'finance', 'Sohaib', 'Finance', 1, NULL),
(16, 'sohaib.akram@immensecode.ai', '$2b$12$39dzoriJmattaN.JCxeeo.g2DH.SUgfOmXlEBuPoLLAxuG/ARWT4G', 'manager', 'Sohaib', 'ImmenseCode', 1, '29239524-c3f8-45dc-bcd7-57aca25255e3'),
(17, 'amjad.ali@ajcl.net', '$2b$12$ixM3QLGQR/l34O4hLK9aJOcqnPFKDVmWvCVhmQzAPsxK1A9AhqMzS', 'senior_manager', 'Amjad', 'ImmenseCode', 0, '8aee5f06-68db-4649-944f-d3e1327a193d'),
(18, 'muhammad.salman@ajcl.net', '$2b$12$izr9ZEoZ/GNcx4YT2VS/2OvtIademfnUah9UqfiPIpJzEwAj1WMOq', 'employee', 'Salman', 'ImmenseCode', 0, 'b16ebcca-cc5d-4cee-8d61-f20462d6718d'),
(19, 'sohaibstylo03332140546@gmail.com', '$2b$12$RB/zeALmUjbaYfawS2QAcOusEcklOykpT.JoE6c5Rs7oyISmofQOa', 'employee', 'Sohaib', 'ImmenseCode', 1, 'be2e3e80-6aac-48b9-a037-5fd501ea919f');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `request_status_log`
--
ALTER TABLE `request_status_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `request_status_log`
--
ALTER TABLE `request_status_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
