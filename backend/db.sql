CREATE DATABASE `reisender-db` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `feature_embeddings` (
  `feature_id` int NOT NULL,
  `word_vector` text NOT NULL,
  PRIMARY KEY (`feature_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `featureinfo` (
  `feature_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `image_url` text NOT NULL,
  PRIMARY KEY (`feature_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `logininfo` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` text NOT NULL,
  `firstlogin` text NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `place_embeddings` (
  `place_id` int NOT NULL,
  `word_vector` text NOT NULL,
  PRIMARY KEY (`place_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `placeinfo` (
  `place_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `image_url` text NOT NULL,
  PRIMARY KEY (`place_id`),
  UNIQUE KEY `name_id` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=402 DEFAULT CHARSET=utf8mb3;

CREATE TABLE `user_embeddings` (
  `user_id` int NOT NULL,
  `avg_num` int NOT NULL,
  `word_vector` text NOT NULL,
  `wish_vector` text,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `userinfo` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `visited_list` text,
  `wish_list` text,
  `feature_list` text,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb3;
