<?php

namespace App\Entity;

use App\Repository\TicketRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: TicketRepository::class)]
class Ticket
{

    public function __construct()
    {
        $this->ticketAnalysis = new ArrayCollection();
    }

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    /**
     * @var Collection<int, TicketAnalysis>
     */
    #[ORM\OneToMany(targetEntity: TicketAnalysis::class, mappedBy: 'ticket', cascade: ['persist'], orphanRemoval: true)]
    private Collection $ticketAnalysis;

    #[ORM\Column(type: 'text')]
    private ?string $content = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getContent(): ?string
    {
        return $this->content;
    }

    public function setContent(string $content): static
    {
        $this->content = $content;
        return $this;
    }

    /**
     * @return Collection<int, TicketAnalysis>
     */
    public function getTicketAnalysis(): Collection
    {
        return $this->ticketAnalysis;
    }

    public function addTicketAnalysi(TicketAnalysis $ticketAnalysi): static
    {
        if (!$this->ticketAnalysis->contains($ticketAnalysi)) {
            $this->ticketAnalysis->add($ticketAnalysi);
            $ticketAnalysi->setTicket($this);
        }

        return $this;
    }

    public function removeTicketAnalysi(TicketAnalysis $ticketAnalysi): static
    {
        if ($this->ticketAnalysis->removeElement($ticketAnalysi)) {
            // set the owning side to null (unless already changed)
            if ($ticketAnalysi->getTicket() === $this) {
                $ticketAnalysi->setTicket(null);
            }
        }

        return $this;
    }
}
