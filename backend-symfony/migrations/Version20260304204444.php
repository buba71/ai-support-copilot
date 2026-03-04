<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20260304204444 extends AbstractMigration
{
    public function getDescription(): string
    {
        return '';
    }

    public function up(Schema $schema): void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE ticket_analysis ADD recommended_policy VARCHAR(255) DEFAULT NULL');
        $this->addSql('ALTER TABLE ticket_analysis ADD escalation_required BOOLEAN DEFAULT false NOT NULL');
        $this->addSql('ALTER TABLE ticket_analysis ADD justification TEXT DEFAULT NULL');
        $this->addSql('ALTER TABLE ticket_analysis ADD metadata JSON DEFAULT NULL');
    }

    public function down(Schema $schema): void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->addSql('ALTER TABLE ticket_analysis DROP recommended_policy');
        $this->addSql('ALTER TABLE ticket_analysis DROP escalation_required');
        $this->addSql('ALTER TABLE ticket_analysis DROP justification');
        $this->addSql('ALTER TABLE ticket_analysis DROP metadata');
    }
}
