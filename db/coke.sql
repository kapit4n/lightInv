-- phpMyAdmin SQL Dump
-- version 4.3.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Aug 25, 2015 at 08:27 PM
-- Server version: 5.6.24
-- PHP Version: 5.6.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `coke`
--

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE IF NOT EXISTS `address` (
  `id` int(11) NOT NULL,
  `street` varchar(10) NOT NULL,
  `city` varchar(10) NOT NULL,
  `number` int(10) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`id`, `street`, `city`, `number`) VALUES
(1, 'Main Stree', 'City 1', 1616),
(2, 'st2', 'City 2', 1212);

-- --------------------------------------------------------

--
-- Table structure for table `car`
--

CREATE TABLE IF NOT EXISTS `car` (
  `id` int(11) NOT NULL,
  `type` varchar(30) NOT NULL,
  `model` varchar(20) NOT NULL,
  `capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `car_driver`
--

CREATE TABLE IF NOT EXISTS `car_driver` (
  `id` int(11) NOT NULL,
  `car_id` int(11) NOT NULL,
  `driver_id` int(11) NOT NULL,
  `assigned_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

CREATE TABLE IF NOT EXISTS `driver` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `driver`
--

INSERT INTO `driver` (`id`, `name`) VALUES
(1, 'Driver 1'),
(2, 'Driver 2'),
(3, 'Driver 3'),
(4, 'Driver 4'),
(5, 'Driver 5');

-- --------------------------------------------------------

--
-- Table structure for table `package`
--

DROP TABLE package;

CREATE TABLE IF NOT EXISTS `package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `shiping_date` date NOT NULL,
  `product_quantity` int(11) NOT NULL DEFAULT 0,
  `driver_id` int(11) NOT NULL,
  `destiny` int(11) NOT NULL,
  `status` enum('new','shipping','dispatched','verified','closed','pending','packaging', 'held', 'abandoned') NOT NULL DEFAULT 'new',
  `storekeeper` int(11) NOT NULL DEFAULT 0,
  `customer` int(11) NOT NULL DEFAULT 0,
  `owner` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `package`
--

INSERT INTO `package` (`id`, `created_at`, `shiping_date`, `product_quantity`, `driver_id`, `destiny`, `status`, `storekeeper`, `customer`, `owner`) VALUES
(24, '2015-08-21 21:42:56', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(25, '2015-08-21 21:48:19', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(26, '2015-08-22 00:38:58', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(27, '2015-08-22 00:39:07', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(28, '2015-08-22 00:40:01', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(29, '2015-08-22 00:40:43', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(30, '2015-08-24 14:25:21', '0000-00-00', 0, 0, 0, 'new', 0, 0, 0),
(31, '2015-08-24 20:03:17', '0000-00-00', 0, 0, 0, 'new', 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `package_item`
--

DROP TABLE package_item;

CREATE TABLE IF NOT EXISTS `package_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(30) NOT NULL,
  `package_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `quantity_filled` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `package_item`
--

INSERT INTO `package_item` (`id`, `product_id`, `product_name`, `package_id`, `quantity`) VALUES
(68, 1, 'ss', 24, 0),
(69, 2, 'Product 2', 24, 0),
(70, 2, 'Product 2', 25, 0),
(71, 3, 'Name', 25, 0),
(72, 1, 'ss', 25, 0),
(73, 1, 'ss', 24, 0),
(74, 2, 'Product 2', 24, 0),
(75, 1, 'ss', 28, 66),
(76, 1, 'ss', 29, 3),
(77, 2, 'Product 2', 29, 5),
(78, 3, 'Name', 29, 3),
(79, 1, 'ss', 29, 0),
(80, 2, 'Product 2', 29, 0),
(81, 2, 'Product 2', 29, 0),
(82, 3, 'Name', 29, 0),
(83, 1, 'ss', 25, 77),
(84, 1, 'ss', 26, 22),
(85, 2, 'Product 2', 26, 22),
(86, 1, 'ss', 27, 11),
(87, 2, 'Product 2', 27, 22),
(88, 2, 'Product 2', 28, 2),
(89, 1, 'ss', 31, 22);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `code` varchar(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `code`, `quantity`) VALUES
(1, 'ss', '333', 0),
(2, 'Product 2', 'w333', 100),
(3, 'Name', 'r444', 22),
(4, 'Pura Vida', 'PV', 28);

-- --------------------------------------------------------

--
-- Table structure for table `storekeeper`
--

CREATE TABLE IF NOT EXISTS `storekeeper` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL DEFAULT 'store keeper'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL,
  `display_name` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `login` varchar(30) NOT NULL,
  `user_type` enum('customer','driver','storekeeper','') NOT NULL,
  `password` varchar(50) NOT NULL DEFAULT 'password'
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `display_name`, `email`, `login`, `user_type`, `password`) VALUES
(1, 'user 1', 'luis@gmail.com', 'luis', 'customer', 'password'),
(2, 'user 2', 'user2', 'luis2', 'driver', 'password2'),
(3, 'User 3', 'user3', 'luis3', 'storekeeper', 'pass');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `car`
--
ALTER TABLE `car`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `car_driver`
--
ALTER TABLE `car_driver`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `driver`
--
ALTER TABLE `driver`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `package`
--
ALTER TABLE `package`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `package_item`
--
ALTER TABLE `package_item`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `storekeeper`
--
ALTER TABLE `storekeeper`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `login` (`login`), ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address`
--
ALTER TABLE `address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `car`
--
ALTER TABLE `car`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `car_driver`
--
ALTER TABLE `car_driver`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `driver`
--
ALTER TABLE `driver`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `package`
--
ALTER TABLE `package`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=32;
--
-- AUTO_INCREMENT for table `package_item`
--
ALTER TABLE `package_item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=90;
--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `storekeeper`
--
ALTER TABLE `storekeeper`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
