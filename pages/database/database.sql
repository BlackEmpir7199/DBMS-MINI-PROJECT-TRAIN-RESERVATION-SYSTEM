//A consolidated SQL commands to create all the table of the project
//TOOL - MySQL Workbench

CREATE DATABASE train_reservation_db;
USE train_reservation_db;

CREATE TABLE `admins` (
  `email` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `username` (`name`)
)

CREATE TABLE `passengers` (
  `passenger_id` int NOT NULL AUTO_INCREMENT,
  `booking_id` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`passenger_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `passengers_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`)
)

CREATE TABLE `stations` (
  `station_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`station_id`)
)

CREATE TABLE `bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int DEFAULT NULL,
  `date_of_travel` date NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `train_id` (`train_id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`)
)

CREATE TABLE `users` (
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE KEY `email` (`email`)
)

CREATE TABLE `trains` (
  `train_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `from_station` int DEFAULT NULL,
  `to_station` int DEFAULT NULL,
  `departure_time` time NOT NULL,
  `arrival_time` time NOT NULL,
  `total_seats` int NOT NULL,
  `available_seats` int NOT NULL,
  PRIMARY KEY (`train_id`),
  KEY `from_station` (`from_station`),
  KEY `to_station` (`to_station`),
  CONSTRAINT `trains_ibfk_1` FOREIGN KEY (`from_station`) REFERENCES `stations` (`station_id`),
  CONSTRAINT `trains_ibfk_2` FOREIGN KEY (`to_station`) REFERENCES `stations` (`station_id`)
)