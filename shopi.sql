CREATE DATABASE Tesco;
SHOW DATABASES;
USE Tesco;
SHOW TABLES;

CREATE TABLE `Tesco`.`Shop` (
  `idShop` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  UNIQUE INDEX `idShop_UNIQUE` (`idShop` ASC));
  
  CREATE TABLE `Tesco`.`Product` (
  `idProduct` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `price` INT NULL,
  PRIMARY KEY (`idProduct`),
  UNIQUE INDEX `idProduct_UNIQUE` (`idProduct` ASC));
  
  CREATE TABLE `Tesco`.`Order` (
  `idOrder` INT NOT NULL AUTO_INCREMENT,
  `price` INT NULL,
  PRIMARY KEY (`idOrder`),
  UNIQUE INDEX `idOrder_UNIQUE` (`idOrder` ASC));
  
  CREATE TABLE `Tesco`.`LineItem` (
  `idLineItem` INT NOT NULL,
  `Price` INT NULL,
  PRIMARY KEY (`idLineItem`),
  UNIQUE INDEX `idLineItem_UNIQUE` (`idLineItem` ASC));
  
INSERT INTO `Tesco`.`Product`
(`idProduct`,
`name`,
`shopId`)
VALUES
(24,
'Maverick Shades',
126),(27,
'YETI',
126);

SELECT *
FROM `Tesco`.`Product`;

SELECT *
FROM `Tesco`.`Product`
RIGHT JOIN `Tesco`.`Shop` ON `Tesco`.`Shop`.name = `Tesco`.`Product`.shopId;


