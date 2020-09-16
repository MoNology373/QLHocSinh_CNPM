-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: studentmanagementdb
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `lastName` tinytext COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `firstName` tinytext COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `gender` tinytext COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `address` varchar(200) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `class_id` int DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id` (`student_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Chu Thiên\r\n',' An','Nữ','2005-12-19','phungthehung84@gmail.com','Huyện Mai Sơn, Sơn La',1),(2,'Nguyễn Thị Thu \r\n','Hà','Nữ','2005-12-11','lethihuong.mss@gmail.com','Thành phố Thái Nguyên, Thái Nguyên',1),(3,'Lê Minh\r\n',' Quân','Nam','2005-01-31','nguyenthikimly0411@gmail.com','Thành phố Thái Nguyên, Thái Nguyên',1),(4,'Trần Thanh\r\n',' Bình','Nam','2005-11-24','nguyenthi189@yahoo.com.vn','Thành phố Thái Nguyên, Thái Nguyên',1),(5,'Nguyễn Huỳnh Nhựt \r\n','Huy','Nan','2005-03-30','hoaiduong321@gmail.com','Thành phố Thái Nguyên, Thái Nguyên',1),(6,'Nguyễn Lê Gia\r\n',' Huy','Nam','2005-10-30','haiantran209@gmail.com','Huyện Chợ Mới, Bắc Kạn',1),(7,'Nguyễn Kông \r\n','Nguyên','Nam','2005-07-20','yenphanngoc93@gmail.com','Thị xã Phúc Yên, Vĩnh Phúc		',2),(8,'Nguyễn Hữu Minh\r\n',' An','Nam','2005-11-21','hanh.ib1010@gmail.com','Huyện Bắc Sơn, Lạng Sơn		',2),(9,'Trần Bách ','Tùng\r\n','Nam','2005-11-29','thuyngashushi@gmail.com','Thành phố Thái Nguyên, Thái Nguyên		',2),(10,'Lê Minh \r\n','Hải','Nam','2005-09-02','chudinhxinh@gmail.com','Huyện Phổ Yên, Thái Nguyên		',2),(11,'Trịnh Hoàng Kỳ \r\n','Anh','Nam','2005-01-10','kientruc07tn@gmail.com','Huyện Tân Yên, Bắc Giang		',2),(12,'Đinh Lan \r\n','Hương','Nữ','2005-04-27','nguyenbabangviet@gmail.com','Thị xã Sông Công, Thái Nguyên		',3),(13,'Bạch Bảo \r\n','Khải','Nam','2005-12-06','hoa11977@gmail.com','Thành phố Thái Nguyên, Thái Nguyên		',3),(14,'Trần Thế \r\n','Hoàng','Nam','2005-05-23','trandangkhoa06591@gmail.com.em','Huyện Phú Lương, Thái Nguyên		',3),(15,'Phạm Thị\r\n','Ba','Nữ','2006-04-08','truongnguyenacc@gmail.com','Huyện Định Hoá, Thái Nguyên		',3),(16,'Đào Thế \r\n','Hiển','Nam','2005-10-12','bemap142@gmail.com','Huyện Bình Liêu, Quảng Ninh		',3),(17,'Nguyễn Thị Anh \r\n','Thư','Nữ','2005-03-19','thaophan1109@gmail.com','Huyện Phổ Yên, Thái Nguyên		',3),(18,'Hoàng Minh \r\n','Anh','Nữ','2005-07-26','huong.wfc@gmail.com','Thành phố Thái Nguyên, Thái Nguyên		',3),(19,'Nguyễn Đức \r\n','Tâm','Nam ','2000-03-20','chanhleockt@gmail.com','Huyện Phú Lương, Thái Nguyên		',4),(20,'Trần Nguyễn Việt \r\n','Thái','Nam','2000-01-04','nguyenhthuy297@gmail.com','Thị xã Sông Công, Thái Nguyên		',4),(21,'Nguyễn Đình \r\n','Cường','Nam','2000-01-10','khoinguonsangtaovn@gmail.com','Thành phố Thái Nguyên, Thái Nguyên		',4),(22,'Nguyễn Đăng \r\n','Đạt','Nam','2000-02-02','dinhquang.vvn@gmail.com','Huyện Định Hoá, Thái Nguyên		',4),(23,'Nguyễn Hoàng \r\n','Nghi','Nữ','2000-10-09','nguyenhien93.hitech@gmail.com','Huyện Đồng Hỷ, Thái Nguyên		',4),(24,'Bùi Thị Mỹ\r\n','Phương','Nữ','2000-01-31','dbloan33@gmail.com','Huyện Đại Từ, Thái Nguyên		',4);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-16 20:35:04
