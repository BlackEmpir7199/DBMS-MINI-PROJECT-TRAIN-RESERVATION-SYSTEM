-- Create Users Table
CREATE TABLE users (
  user_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  PRIMARY KEY (user_id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create Stations Table
CREATE TABLE stations (
  station_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (station_id)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create Trains Table
CREATE TABLE trains (
  train_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  available_seats INT NOT NULL,
  departure_time TIME NOT NULL,
  arrival_time TIME NOT NULL,
  PRIMARY KEY (train_id)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create Bookings Table
CREATE TABLE bookings (
  booking_id INT NOT NULL AUTO_INCREMENT,
  user_id INT DEFAULT NULL,
  train_id INT DEFAULT NULL,
  date_of_travel DATE NOT NULL,
  PRIMARY KEY (booking_id),
  KEY user_id (user_id),
  KEY train_id (train_id),
  CONSTRAINT bookings_ibfk_1 FOREIGN KEY (user_id) REFERENCES users (user_id),
  CONSTRAINT bookings_ibfk_2 FOREIGN KEY (train_id) REFERENCES trains (train_id)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create Tickets Table
CREATE TABLE tickets (
  ticket_id INT NOT NULL AUTO_INCREMENT,
  booking_id INT DEFAULT NULL,
  train_id INT DEFAULT NULL,
  user_id INT DEFAULT NULL,
  date_of_travel DATE NOT NULL,
  PRIMARY KEY (ticket_id),
  KEY train_id (train_id),
  KEY user_id (user_id),
  KEY fk_tickets_bookings (booking_id),
  CONSTRAINT fk_tickets_bookings FOREIGN KEY (booking_id) REFERENCES bookings (booking_id) ON DELETE CASCADE,
  CONSTRAINT tickets_ibfk_1 FOREIGN KEY (booking_id) REFERENCES bookings (booking_id),
  CONSTRAINT tickets_ibfk_2 FOREIGN KEY (train_id) REFERENCES trains (train_id),
  CONSTRAINT tickets_ibfk_3 FOREIGN KEY (user_id) REFERENCES users (user_id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Procedure to Book Ticket
CREATE DEFINER=`root`@`localhost` PROCEDURE book_ticket(
    IN p_user_id INT,
    IN p_train_id INT,
    IN p_date_of_travel DATE)
BEGIN
    INSERT INTO bookings (user_id, train_id, date_of_travel)
    VALUES (p_user_id, p_train_id, p_date_of_travel);
END;

-- Trigger After Insert on Bookings
CREATE DEFINER=`root`@`localhost` TRIGGER bookings_AFTER_INSERT AFTER INSERT ON bookings FOR EACH ROW BEGIN
    UPDATE trains
    SET available_seats = available_seats - 1
    WHERE train_id = NEW.train_id;
END;

-- Trigger After Delete on Bookings
CREATE DEFINER=`root`@`localhost` TRIGGER bookings_AFTER_DELETE AFTER DELETE ON bookings FOR EACH ROW BEGIN
    DELETE FROM tickets
    WHERE booking_id = OLD.booking_id;
END;
