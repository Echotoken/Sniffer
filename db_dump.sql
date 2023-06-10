-- MySQL dump 10.13  Distrib 5.7.41, for Linux (x86_64)
--
-- Host: localhost    Database: SNIFFER
-- ------------------------------------------------------
-- Server version	5.7.41

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
-- Table structure for table `choose_model`
--

DROP TABLE IF EXISTS `choose_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `choose_model` (
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`model`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `local_attack`
--

DROP TABLE IF EXISTS `local_attack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `local_attack` (
  `local_name` varchar(100) NOT NULL,
  `attacked_model` varchar(100) NOT NULL,
  `probe_modules` varchar(100) NOT NULL,
  `attack_datasets` varchar(100) NOT NULL,
  `upload_model` varchar(100) NOT NULL,
  PRIMARY KEY (`local_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `local_result`
--

DROP TABLE IF EXISTS `local_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `local_result` (
  `tree_num` int(100) DEFAULT NULL,
  `svm_num` int(100) DEFAULT NULL,
  `linear_num` int(100) DEFAULT NULL,
  `nn_num` int(100) DEFAULT NULL,
  `tree_time` int(100) DEFAULT NULL,
  `svm_time` int(100) DEFAULT NULL,
  `linear_time` int(100) DEFAULT NULL,
  `nn_time` int(100) DEFAULT NULL,
  `tree_conf` float DEFAULT NULL,
  `svm_conf` float DEFAULT NULL,
  `linear_conf` float DEFAULT NULL,
  `nn_conf` float DEFAULT NULL,
  `cnn_conf` float DEFAULT NULL,
  `rnn_conf` float DEFAULT NULL,
  `gnn_conf` float DEFAULT NULL,
  `local_name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`local_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mlaas_attack`
--

DROP TABLE IF EXISTS `mlaas_attack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mlaas_attack` (
  `mlaas_name` varchar(100) NOT NULL,
  `cloud` varchar(10) NOT NULL,
  `probe_module` varchar(100) NOT NULL,
  `api` varchar(10000) NOT NULL,
  `sample_space` varchar(100) NOT NULL,
  `attack_datasets` varchar(100) NOT NULL,
  `feature_num` varchar(100) NOT NULL,
  `feature_range` varchar(100) NOT NULL,
  PRIMARY KEY (`mlaas_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mlaas_result`
--

DROP TABLE IF EXISTS `mlaas_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mlaas_result` (
  `tree_num` int(100) DEFAULT NULL,
  `svm_num` int(100) DEFAULT NULL,
  `linear_num` int(100) DEFAULT NULL,
  `nn_num` int(100) DEFAULT NULL,
  `tree_time` int(100) DEFAULT NULL,
  `svm_time` int(100) DEFAULT NULL,
  `linear_time` int(100) DEFAULT NULL,
  `nn_time` int(100) DEFAULT NULL,
  `tree_conf` float DEFAULT NULL,
  `svm_conf` float DEFAULT NULL,
  `linear_conf` float DEFAULT NULL,
  `nn_conf` float DEFAULT NULL,
  `cnn_conf` float DEFAULT NULL,
  `rnn_conf` float DEFAULT NULL,
  `gnn_conf` float DEFAULT NULL,
  `mlaas_name` varchar(100) NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`mlaas_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `register` (
  `username` char(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-18 22:09:09
