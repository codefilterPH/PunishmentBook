from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Creates custom tables for the application.'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # -- EncapsulateToHtmlTag Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `EncapsulateToHtmlTag` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `encap` BOOLEAN DEFAULT TRUE,
                    PRIMARY KEY (`id`)
                );
            """)

            # OutlineIntro Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `OutlineIntro` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `header` VARCHAR(250) NULL,
                    `outline` TEXT NULL,
                    `subsequent` VARCHAR(250) NULL,
                    `keyw_id` INT NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`keyw_id`) REFERENCES `Keywords`(`id`) ON DELETE CASCADE,
                    UNIQUE (`keyw_id`)
                );
            """)

            # OutlineBody Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `OutlineBody` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `position` SMALLINT DEFAULT 0,
                    `header` VARCHAR(250) NULL,
                    `outline` TEXT NULL,
                    `subsequent` VARCHAR(250) NULL,
                    `keyw_id` INT NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`keyw_id`) REFERENCES `Keywords`(`id`) ON DELETE CASCADE
                );
            """)

            # ContentBody Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS  `ContentBody` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `position` SMALLINT DEFAULT 0,
                    `header` VARCHAR(250) NULL,
                    `section` TEXT NULL,
                    `subsequent` VARCHAR(250) NULL,
                    `keyw_id` INT NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`keyw_id`) REFERENCES `Keywords`(`id`) ON DELETE CASCADE
                );
            """)

            # OutlineConclusion Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `OutlineConclusion` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `header` VARCHAR(250) NULL,
                    `outline` TEXT NULL,
                    `subsequent` VARCHAR(250) NULL,
                    `keyw_id` INT NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`keyw_id`) REFERENCES `Keywords`(`id`) ON DELETE CASCADE,
                    UNIQUE (`keyw_id`)
                );
            """)

            # -- ArtificialIntelligenceList Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `ArtificialIntelligenceList` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `label` VARCHAR(255) NULL DEFAULT 'Chatgpt' UNIQUE,
                    PRIMARY KEY (`id`)
                );
            """)

            # -- AiModelVariations Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `AiModelVariations` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `ai_id` INT NOT NULL,
                    `variation` VARCHAR(255) NULL,
                    `value` VARCHAR(255) NULL,
                    `is_default` BOOLEAN DEFAULT FALSE,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`ai_id`) REFERENCES `ArtificialIntelligenceList`(`id`),
                    UNIQUE(`variation`, `value`)
                );
            """)

            # -- AIPrimaryAssignment Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `AIPrimaryAssignment` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `content_part` VARCHAR(100) NULL UNIQUE,
                    `ai_model_variation_id` INT NOT NULL,
                    `backup_ai_id` INT NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`ai_model_variation_id`) REFERENCES `AiModelVariations`(`id`),
                    FOREIGN KEY (`backup_ai_id`) REFERENCES `AiModelVariations`(`id`)
                );
            """)

            # -- ScriptTotalPromptCost Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `ScriptTotalPromptCost` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `keyw_id` INT,
                    `content` TEXT,
                    `total` DECIMAL(10,5),
                    `api_key` TEXT,
                    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`)
                );
            """)

            # -- MultilineVariableExtractor Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `MultilineVariableExtractor` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `content_parts_id` INT NOT NULL,
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`content_parts_id`) REFERENCES `AIPrimaryAssignment`(`id`),
                    UNIQUE (`content_parts_id`)
                );
            """)

            # -- VariableValuePair Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `VariableValuePair` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `extractor_id` INT NOT NULL,
                    `variable_name` VARCHAR(255) NOT NULL,
                    `variable_value` VARCHAR(255) DEFAULT '',
                    PRIMARY KEY (`id`),
                    FOREIGN KEY (`extractor_id`) REFERENCES `MultilineVariableExtractor`(`id`)
                );
            """)

            # Feedback to the user
            self.stdout.write(self.style.SUCCESS('Successfully created custom tables.'))
