<?php

namespace App\Entity;

use App\Repository\TicketAnalysisRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: TicketAnalysisRepository::class)]
class TicketAnalysis
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $analysisContent = null;

    #[ORM\Column]
    private ?float $score = null;

    #[ORM\Column]
    private array $sources = [];

    #[ORM\ManyToOne(inversedBy: 'ticketAnalysis')]
    private ?Ticket $ticket = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getAnalysisContent(): ?string
    {
        return $this->analysisContent;
    }

    public function setAnalysisContent(string $analysisContent): static
    {
        $this->analysisContent = $analysisContent;

        return $this;
    }

    public function getScore(): ?float
    {
        return $this->score;
    }

    public function setScore(float $score): static
    {
        $this->score = $score;

        return $this;
    }

    public function getSources(): array
    {
        return $this->sources;
    }

    public function setSources(array $sources): static
    {
        $this->sources = $sources;

        return $this;
    }

    public function getTicket(): ?Ticket
    {
        return $this->ticket;
    }

    public function setTicket(?Ticket $ticket): static
    {
        $this->ticket = $ticket;

        return $this;
    }
}
