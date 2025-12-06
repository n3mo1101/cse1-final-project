-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: techtown
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `price` float NOT NULL,
  `stocks` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Wireless Keyboard','Ergonomic wireless keyboard with numeric keypad',29.99,45),(2,'Optical Mouse','Precision optical mouse with scroll wheel',15.99,80),(3,'USB Flash Drive','64GB USB 3.0 flash drive with high transfer speed',12.99,120),(4,'Desk Lamp','LED desk lamp with adjustable brightness',24.99,35),(5,'Water Bottle','Insulated stainless steel water bottle 1L',19.99,60),(6,'Notebook','Hardcover A5 notebook with 200 pages',8.99,200),(7,'Ballpoint Pen','Pack of 12 blue ink ballpoint pens',4.99,300),(8,'Coffee Mug','Ceramic coffee mug with handle 350ml',6.99,85),(9,'Backpack','Water-resistant backpack with laptop compartment',39.99,25),(10,'Phone Case','Protective phone case with screen protector',9.99,150),(11,'Desk Organizer','Multi-compartment desk organizer for supplies',14.99,40),(12,'Sticky Notes','Pack of 5 colorful sticky notes pads',3.99,180),(13,'Calculator','Scientific calculator with LCD display',18.99,30),(14,'Headphones','Over-ear headphones with comfortable padding',34.99,55),(15,'Power Bank','10000mAh portable power bank with fast charging',27.99,65),(16,'Laptop Stand','Adjustable aluminum laptop stand for ergonomics',32.99,20),(17,'HDMI Cable','6 feet high-speed HDMI cable 4K compatible',7.99,95),(18,'Wireless Charger','Qi-certified fast wireless charging pad',21.99,50),(19,'Webcam','1080p HD webcam with built-in microphone',49.99,15),(20,'Monitor Stand','Universal monitor stand with storage drawer',44.99,18);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-29 21:03:39
