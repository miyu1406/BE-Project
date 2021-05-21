-- MySQL dump 10.13  Distrib 5.7.33, for Linux (x86_64)
--
-- Host: localhost    Database: rest
-- ------------------------------------------------------
-- Server version	5.7.33-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `userreg`
--

DROP TABLE IF EXISTS `userreg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userreg` (
  `iduserreg` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `pass` varchar(45) DEFAULT NULL,
  `cpass` varchar(45) DEFAULT NULL,
  `height` varchar(45) DEFAULT NULL,
  `weight` varchar(45) DEFAULT NULL,
  `age` varchar(45) DEFAULT NULL,
  `contact` varchar(45) DEFAULT NULL,
  `cat` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`iduserreg`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userreg`
--

LOCK TABLES `userreg` WRITE;
/*!40000 ALTER TABLE `userreg` DISABLE KEYS */;
INSERT INTO `userreg` VALUES (1,'ram','ram123@gmail.com','Ram@1234','Ram@1234','165','45','34','9987654321','Young'),(2,'Akshu','akshu@gmail.com','Akshu@123','Akshu@123','156','56','28','7020757594',''),(3,'Akshay Gund','gundtime@gmail.com','Daaku@2','Daaku@2','180','70','25','9370192306',''),(4,'Akash','a2k@gmail.com','Akash@123','Akash@123','155','50','22','8698580580',''),(5,'abcd','abcd@gmail.com','Abcd@123','Abcd@123','160','60','56','8888888888','0'),(6,'qwer','qwer@gmail.com','qwer@123','qwer@123','123','23','34','9887776655','0'),(7,'dse','dse@gmail.com','Dse@123','Dse@123','178','78','69','7020757594','0'),(8,'Azq','azq@gmail.com','Azq@123','Azq@123','156','56','67','9876543334','0'),(9,'abc','abc@gmail.com','abc@1234','abc@1234','100','10','34','9370192306','Children'),(10,'ac','ac@gmail.com','Ac@123','Ac@123','140','40','38','7020757594','Oldage'),(11,'Karishma','karishma@gmail.com','Karishma@123','Karishma@123','162','44','22','9887776655','0'),(12,'Kari','kari@gmail.com','kari@123','kari@123','162','44','22','9887776655','Young'),(13,'Akash Kharat','akash@gmail.com','Akash@123','Akash@123','170','78','82','7020757594','0'),(14,'saista','saista@gmail.com','saista@123','Saista@123','151','66','23','9988776655','Young'),(15,'supriya','supriya@gmail.com','supriya@123','supriya@123','152','45','10','8877766554','Children'),(16,'saloni','saloni@gmail.com','Saloni@123','Saloni@123','154','65','60','7766554433','0'),(17,'sonali','sonali@gmail.com','Sonali@123','Sonali@123','154','45','67','9988773344','Oldage');
/*!40000 ALTER TABLE `userreg` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-27 10:51:07
