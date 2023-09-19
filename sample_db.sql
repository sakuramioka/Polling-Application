-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: sample_db
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `example_post_1`
--

DROP TABLE IF EXISTS `example_post_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `example_post_1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `class` varchar(255) DEFAULT NULL,
  `section` varchar(255) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `votes` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `example_post_1`
--

LOCK TABLES `example_post_1` WRITE;
/*!40000 ALTER TABLE `example_post_1` DISABLE KEYS */;
INSERT INTO `example_post_1` VALUES (1,'Cand. With Image 1','X','A','D:/Poll/Candidate_Images/CandidateExample1.png',0),(2,'Cand. Without Image 1','X','B','imagesplaceholder.png',0),(3,'Cand. Without Image 2','XII','C','imagesplaceholder.png',0),(4,'Cand. With Image 2','XI','C','D:/Poll/Candidate_Images/CandidateExample2.png',0),(5,'Cand. Without Image 3','XII','D','',0);
/*!40000 ALTER TABLE `example_post_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `example_post_2`
--

DROP TABLE IF EXISTS `example_post_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `example_post_2` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `class` varchar(255) DEFAULT NULL,
  `section` varchar(255) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `votes` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `example_post_2`
--

LOCK TABLES `example_post_2` WRITE;
/*!40000 ALTER TABLE `example_post_2` DISABLE KEYS */;
INSERT INTO `example_post_2` VALUES (1,'Candidate 1','XII','A','D:/Poll/Candidate_Images/CandidateExample1.png',0),(2,'Candidate 2','XI','B','imagesplaceholder.png',0),(3,'Candidate 3','XII','D','D:/Poll/Candidate_Images/CandidateExample2.png',0);
/*!40000 ALTER TABLE `example_post_2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'sample_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-19 17:26:48
