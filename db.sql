/*
Navicat MySQL Data Transfer

Source Server         : 120.79.182.28_3306
Source Server Version : 50731
Source Host           : 120.79.182.28:3306
Source Database       : subscribe

Target Server Type    : MYSQL
Target Server Version : 50731
File Encoding         : 65001

Date: 2021-05-16 22:47:23
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for addr
-- ----------------------------
DROP TABLE IF EXISTS `addr`;
CREATE TABLE `addr` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4;
