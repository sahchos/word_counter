CREATE TABLE `words` (
    `pk` VARCHAR(255) CHARACTER SET utf8 NOT NULL,
    `word` VARCHAR(255) CHARACTER SET utf8 NOT NULL,
    `count` INT NOT NULL,
    PRIMARY KEY (`pk`)
);

CREATE DATABASE IF NOT EXISTS `octopus_test`;
USE `octopus_test`;
CREATE TABLE `words` (
    `pk` VARCHAR(255) CHARACTER SET utf8 NOT NULL,
    `word` VARCHAR(255) CHARACTER SET utf8 NOT NULL,
    `count` INT NOT NULL,
    PRIMARY KEY (`pk`)
);
