<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20260202203906 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE ticket ADD content TEXT NOT NULL');
        $this->addSql('ALTER TABLE ticket_analysis ADD summary TEXT NOT NULL');
        $this->addSql('ALTER TABLE ticket_analysis ADD urgency VARCHAR(255) NOT NULL');
        $this->addSql('ALTER TABLE ticket_analysis RENAME COLUMN analysis_content TO category');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE ticket DROP content');
        $this->addSql('ALTER TABLE ticket_analysis ADD analysis_content VARCHAR(255) NOT NULL');
        $this->addSql('ALTER TABLE ticket_analysis DROP summary');
        $this->addSql('ALTER TABLE ticket_analysis DROP category');
        $this->addSql('ALTER TABLE ticket_analysis DROP urgency');
    }
}
