-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema web project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema web project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `web project` DEFAULT CHARACTER SET latin1 ;
USE `web project` ;

-- -----------------------------------------------------
-- Table `web project`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` VARCHAR(45) NULL DEFAULT NULL,
  `read_access_users` JSON NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `web project`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `web project`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` LONGTEXT NULL DEFAULT NULL,
  `sender_id` INT(11) NOT NULL,
  `receiver_username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users_idx` (`sender_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users`
    FOREIGN KEY (`sender_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `web project`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `text` LONGTEXT NOT NULL,
  `users_id` INT(11) NOT NULL,
  `up_vote` INT(11) NOT NULL,
  `down_vote` INT(11) NOT NULL,
  `categories_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_topics_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `web project`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `web project`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(455) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `topics_id` INT(11) NOT NULL,
  `is_best_reply` TINYINT(4) NOT NULL,
  `upvotes` INT(11) NULL DEFAULT NULL,
  `downvotes` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replies_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_replies_topics1_idx` (`topics_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topics_id`)
    REFERENCES `web project`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `web project`.`reactions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`reactions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_id` INT(11) NOT NULL,
  `replies_id` INT(11) NOT NULL,
  `reaction` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reactions_users_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_reactions_replies1_idx` (`replies_id` ASC) VISIBLE,
  CONSTRAINT `fk_reactions_replies1`
    FOREIGN KEY (`replies_id`)
    REFERENCES `web project`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reactions_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `web project`.`users_has_replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`users_has_replies` (
  `users_id` INT(11) NOT NULL,
  `replies_id` INT(11) NOT NULL,
  `reaction` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`users_id`, `replies_id`),
  INDEX `fk_users_has_replies_replies1_idx` (`replies_id` ASC) VISIBLE,
  INDEX `fk_users_has_replies_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_replies_replies1`
    FOREIGN KEY (`replies_id`)
    REFERENCES `web project`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_replies_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
