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
CREATE SCHEMA IF NOT EXISTS `web project` ;
USE `web project` ;

-- -----------------------------------------------------
-- Table `web project`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`categories` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `is_private` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`conversations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`conversations` (
  `id` INT(11) NOT NULL,
  `receiver` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`users` (
  `id` INT(11) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`topics` (
  `id` INT(11) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `text` LONGTEXT NOT NULL,
  `users_id` INT(11) NOT NULL,
  `up_vote` INT(11) NOT NULL,
  `down_vote` INT(11) NOT NULL,
  `categories_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `users_id`, `categories_id`),
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
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`replies` (
  `id` INT(11) NOT NULL,
  `text` VARCHAR(455) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `topics_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `users_id`, `topics_id`),
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
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`down_vote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`down_vote` (
  `id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `replies_id` INT(11) NOT NULL,
  `replies_users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `users_id`, `replies_id`, `replies_users_id`),
  INDEX `fk_down_vote_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_down_vote_replies1_idx` (`replies_id` ASC, `replies_users_id` ASC) VISIBLE,
  CONSTRAINT `fk_down_vote_replies1`
    FOREIGN KEY (`replies_id` , `replies_users_id`)
    REFERENCES `web project`.`replies` (`id` , `users_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_down_vote_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`messages` (
  `id` INT(11) NOT NULL,
  `text` LONGTEXT NOT NULL,
  `users_id` INT(11) NOT NULL,
  `conversations_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `users_id`, `conversations_id`),
  INDEX `fk_messages_users_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_messages_conversations1_idx` (`conversations_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_conversations1`
    FOREIGN KEY (`conversations_id`)
    REFERENCES `web project`.`conversations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`up_vote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`up_vote` (
  `id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `replies_id` INT(11) NOT NULL,
  `replies_users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `users_id`, `replies_id`, `replies_users_id`),
  INDEX `fk_up_vote_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_up_vote_replies1_idx` (`replies_id` ASC, `replies_users_id` ASC) VISIBLE,
  CONSTRAINT `fk_up_vote_replies1`
    FOREIGN KEY (`replies_id` , `replies_users_id`)
    REFERENCES `web project`.`replies` (`id` , `users_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_up_vote_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web project`.`users_has_conversations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web project`.`users_has_conversations` (
  `users_id` INT(11) NOT NULL,
  `conversations_id` INT(11) NOT NULL,
  PRIMARY KEY (`users_id`, `conversations_id`),
  INDEX `fk_users_has_conversations_conversations1_idx` (`conversations_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_conversations_conversations1`
    FOREIGN KEY (`conversations_id`)
    REFERENCES `web project`.`conversations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_conversations_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

