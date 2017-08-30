-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 30, 2017 at 02:38 PM
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
-- Table structure for table `tempusers`
--

CREATE TABLE `tempusers` (
  `id` bigint(255) UNSIGNED NOT NULL,
  `email` varchar(512) NOT NULL,
  `pass` varchar(128) NOT NULL,
  `fname` varchar(512) NOT NULL,
  `lname` varchar(512) DEFAULT NULL,
  `authlvl` int(8) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tempusers`
--

INSERT INTO `tempusers` (`id`, `email`, `pass`, `fname`, `lname`, `authlvl`) VALUES
(1, 'simrankashyap307@gmail.com', 'f18f057ea44a945a083a00e6fcc11637d186042d', 'Simran', 'Kashyap', 1),
(3, 'sahil@gmail.com', 'f18f057ea44a945a083a00e6fcc11637d186042d', 'Sahil', 'Kumar', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tempusers`
--
ALTER TABLE `tempusers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fname` (`fname`(255)),
  ADD KEY `email` (`email`(255));

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tempusers`
--
ALTER TABLE `tempusers`
  MODIFY `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
