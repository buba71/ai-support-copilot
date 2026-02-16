<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\TicketAiAnalysisFeedbackRepository;
use App\Enum\AiFeedbackDecision;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: TicketAiAnalysisFeedbackRepository::class)]
class TicketAiAnalysisFeedback
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    /**
     * Analyse IA concernée
     */
    #[ORM\ManyToOne(targetEntity: TicketAnalysis::class, inversedBy: 'feedbacks')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private TicketAnalysis $analysis;

    /**
     * Décision humaine (enum)
     */
    #[ORM\Column(enumType: AiFeedbackDecision::class)]
    private AiFeedbackDecision $decision;

    /**
     * Commentaire libre (optionnel)
     */
    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $comment;

    /**
     * Date de création (immutable)
     */
    #[ORM\Column]
    private \DateTimeImmutable $createdAt;

    public function __construct(
        TicketAnalysis $analysis,
        AiFeedbackDecision $decision,
        ?string $comment = null
    ) {
        $this->analysis = $analysis;
        $this->decision = $decision;
        $this->comment = $comment;
        $this->createdAt = new \DateTimeImmutable();
    }

    // --------------------
    // Getters uniquement
    // --------------------

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getAnalysis(): TicketAnalysis
    {
        return $this->analysis;
    }

    public function getDecision(): AiFeedbackDecision
    {
        return $this->decision;
    }

    public function getComment(): ?string
    {
        return $this->comment;
    }

    public function getCreatedAt(): \DateTimeImmutable
    {
        return $this->createdAt;
    }
}