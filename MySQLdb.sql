-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema handy_helper
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema handy_helper
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `handy_helper` DEFAULT CHARACTER SET utf8 ;
USE `handy_helper` ;

-- -----------------------------------------------------
-- Table `handy_helper`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `handy_helper`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email_address` VARCHAR(200) NULL,
  `password_hash` VARCHAR(255) NULL,
  `username` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `handy_helper`.`jobs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `handy_helper`.`jobs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NULL,
  `description` VARCHAR(255) NULL,
  `location` VARCHAR(100) NULL,
  `category` VARCHAR(45) NULL,
  `other` VARCHAR(45) NULL,
  `posted_by` INT NOT NULL,
  `claimed_by` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_jobs_users_idx` (`posted_by` ASC) VISIBLE,
  INDEX `fk_jobs_users1_idx` (`claimed_by` ASC) VISIBLE,
  CONSTRAINT `fk_jobs_users`
    FOREIGN KEY (`posted_by`)
    REFERENCES `handy_helper`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jobs_users1`
    FOREIGN KEY (`claimed_by`)
    REFERENCES `handy_helper`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
