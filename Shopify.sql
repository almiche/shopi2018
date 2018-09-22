-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: Tesco
-- ------------------------------------------------------
-- Server version	5.7.21

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
-- Table structure for table `LineItem`
--

DROP TABLE IF EXISTS `LineItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LineItem` (
  `idLineItem` int(11) NOT NULL,
  `Price` int(11) DEFAULT NULL,
  PRIMARY KEY (`idLineItem`),
  UNIQUE KEY `idLineItem_UNIQUE` (`idLineItem`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LineItem`
--

LOCK TABLES `LineItem` WRITE;
/*!40000 ALTER TABLE `LineItem` DISABLE KEYS */;
/*!40000 ALTER TABLE `LineItem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order`
--

DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Order` (
  `idOrder` int(11) NOT NULL AUTO_INCREMENT,
  `price` int(11) DEFAULT NULL,
  PRIMARY KEY (`idOrder`),
  UNIQUE KEY `idOrder_UNIQUE` (`idOrder`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order`
--

LOCK TABLES `Order` WRITE;
/*!40000 ALTER TABLE `Order` DISABLE KEYS */;
/*!40000 ALTER TABLE `Order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order_Line_items_junction`
--

DROP TABLE IF EXISTS `Order_Line_items_junction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Order_Line_items_junction` (
  `idOrder` int(11) DEFAULT NULL,
  `idLineItem` int(11) DEFAULT NULL,
  KEY `idOrder_idx` (`idOrder`),
  KEY `idLineItem_idx` (`idLineItem`),
  CONSTRAINT `idLineItem` FOREIGN KEY (`idLineItem`) REFERENCES `LineItem` (`idLineItem`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idOrder` FOREIGN KEY (`idOrder`) REFERENCES `Order` (`idOrder`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order_Line_items_junction`
--

LOCK TABLES `Order_Line_items_junction` WRITE;
/*!40000 ALTER TABLE `Order_Line_items_junction` DISABLE KEYS */;
/*!40000 ALTER TABLE `Order_Line_items_junction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Product` (
  `idProduct` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  PRIMARY KEY (`idProduct`),
  UNIQUE KEY `idProduct_UNIQUE` (`idProduct`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product_Line_items_junction`
--

DROP TABLE IF EXISTS `Product_Line_items_junction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Product_Line_items_junction` (
  `ProductId` int(11) DEFAULT NULL,
  `LineItemId` int(11) DEFAULT NULL,
  KEY `idLineItem_idx` (`LineItemId`),
  KEY `id_Product` (`ProductId`),
  CONSTRAINT `id_LineItem` FOREIGN KEY (`LineItemId`) REFERENCES `LineItem` (`idLineItem`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_Product` FOREIGN KEY (`ProductId`) REFERENCES `Product` (`idProduct`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product_Line_items_junction`
--

LOCK TABLES `Product_Line_items_junction` WRITE;
/*!40000 ALTER TABLE `Product_Line_items_junction` DISABLE KEYS */;
/*!40000 ALTER TABLE `Product_Line_items_junction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Shop`
--

DROP TABLE IF EXISTS `Shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Shop` (
  `idShop` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  UNIQUE KEY `idShop_UNIQUE` (`idShop`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Shop`
--

LOCK TABLES `Shop` WRITE;
/*!40000 ALTER TABLE `Shop` DISABLE KEYS */;
/*!40000 ALTER TABLE `Shop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Shop_Orders_junction`
--

DROP TABLE IF EXISTS `Shop_Orders_junction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Shop_Orders_junction` (
  `shopId` int(11) DEFAULT NULL,
  `orderId` int(11) DEFAULT NULL,
  KEY `idShop_idx` (`shopId`),
  KEY `idOrder_idx` (`orderId`),
  CONSTRAINT `orderId` FOREIGN KEY (`orderId`) REFERENCES `Order` (`idOrder`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `shopId` FOREIGN KEY (`shopId`) REFERENCES `Shop` (`idShop`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Shop_Orders_junction`
--

LOCK TABLES `Shop_Orders_junction` WRITE;
/*!40000 ALTER TABLE `Shop_Orders_junction` DISABLE KEYS */;
/*!40000 ALTER TABLE `Shop_Orders_junction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Shop_Products_junction`
--

DROP TABLE IF EXISTS `Shop_Products_junction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Shop_Products_junction` (
  `idShop` int(11) DEFAULT NULL,
  `idProduct` int(11) DEFAULT NULL,
  KEY `idShop_idx` (`idShop`),
  KEY `idProduct_idx` (`idProduct`),
  CONSTRAINT `idProduct` FOREIGN KEY (`idProduct`) REFERENCES `Product` (`idProduct`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idShop` FOREIGN KEY (`idShop`) REFERENCES `Shop` (`idShop`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Shop_Products_junction`
--

LOCK TABLES `Shop_Products_junction` WRITE;
/*!40000 ALTER TABLE `Shop_Products_junction` DISABLE KEYS */;
/*!40000 ALTER TABLE `Shop_Products_junction` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-18 15:19:29
