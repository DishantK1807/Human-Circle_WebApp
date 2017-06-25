-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 25, 2017 at 02:22 AM
-- Server version: 5.6.35
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `yic`
--

-- --------------------------------------------------------

--
-- Table structure for table `candidates`
--

CREATE TABLE `candidates` (
  `id` bigint(255) UNSIGNED NOT NULL,
  `uid` bigint(255) UNSIGNED NOT NULL,
  `fname` varchar(512) NOT NULL,
  `lname` varchar(512) DEFAULT NULL,
  `email` varchar(512) NOT NULL,
  `cv` varchar(1024) DEFAULT NULL,
  `pp` varchar(1024) DEFAULT NULL,
  `ans` varchar(1024) DEFAULT NULL,
  `sel` int(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `candidates`
--

INSERT INTO `candidates` (`id`, `uid`, `fname`, `lname`, `email`, `cv`, `pp`, `ans`, `sel`) VALUES
(1, 2, 'Arpit', 'Nandwani', 'arpit.nandwani@gmail.com', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `final`
--

CREATE TABLE `final` (
  `id` bigint(255) UNSIGNED NOT NULL,
  `uid` bigint(255) UNSIGNED NOT NULL,
  `fname` varchar(512) NOT NULL,
  `lname` varchar(512) DEFAULT NULL,
  `email` varchar(512) NOT NULL,
  `cv` varchar(1024) DEFAULT NULL,
  `pp` varchar(1024) DEFAULT NULL,
  `ans` varchar(1024) DEFAULT NULL,
  `sel` int(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `selected`
--

CREATE TABLE `selected` (
  `id` bigint(255) UNSIGNED NOT NULL,
  `uid` bigint(255) UNSIGNED NOT NULL,
  `fname` varchar(512) NOT NULL,
  `lname` varchar(512) DEFAULT NULL,
  `email` varchar(512) NOT NULL,
  `cv` varchar(1024) DEFAULT NULL,
  `pp` varchar(1024) DEFAULT NULL,
  `ans` varchar(1024) DEFAULT NULL,
  `sel` int(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tempusers`
--

CREATE TABLE `tempusers` (
  `id` bigint(255) UNSIGNED NOT NULL,
  `uname` varchar(128) NOT NULL,
  `pass` varchar(128) NOT NULL,
  `fname` varchar(512) NOT NULL,
  `lname` varchar(512) DEFAULT NULL,
  `email` varchar(512) NOT NULL,
  `authlvl` int(8) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tempusers`
--

INSERT INTO `tempusers` (`id`, `uname`, `pass`, `fname`, `lname`, `email`, `authlvl`) VALUES
(1, 'simipinni', 'f18f057ea44a945a083a00e6fcc11637d186042d', 'Simran', 'Kashyap', 'simrankashyap307@gmail.com', 1),
(3, 'sahil', 'f18f057ea44a945a083a00e6fcc11637d186042d', 'Sahil', 'Kumar', 'sahil@gmail.com', 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(255) UNSIGNED NOT NULL,
  `uname` varchar(128) NOT NULL,
  `pass` varchar(128) NOT NULL,
  `fname` varchar(512) NOT NULL,
  `lname` varchar(512) DEFAULT NULL,
  `email` varchar(512) NOT NULL,
  `authlvl` int(8) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `uname`, `pass`, `fname`, `lname`, `email`, `authlvl`) VALUES
(0, 'su', '308ec91466f28042f2fcde5cf346fd5afd0af824', 'superuser', NULL, 'humancircle@gmail.com', 0),
(1, 'arpit', 'f18f057ea44a945a083a00e6fcc11637d186042d', 'Arpit', 'Nandwani', 'arpit.nandwani@gmail.com', 3),
(2, 'dishant', 'f18f057ea44a945a083a00e6fcc11637d186042d', 'Dishant', 'Khanna', 'dishantkhanna@gmail.com', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `candidates`
--
ALTER TABLE `candidates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`uid`);

--
-- Indexes for table `final`
--
ALTER TABLE `final`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`uid`);

--
-- Indexes for table `selected`
--
ALTER TABLE `selected`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uid` (`uid`);

--
-- Indexes for table `tempusers`
--
ALTER TABLE `tempusers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uname` (`uname`),
  ADD KEY `fname` (`fname`(255));

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uname` (`uname`),
  ADD KEY `fname` (`fname`(255));

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `candidates`
--
ALTER TABLE `candidates`
  MODIFY `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `final`
--
ALTER TABLE `final`
  MODIFY `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `selected`
--
ALTER TABLE `selected`
  MODIFY `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tempusers`
--
ALTER TABLE `tempusers`
  MODIFY `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
