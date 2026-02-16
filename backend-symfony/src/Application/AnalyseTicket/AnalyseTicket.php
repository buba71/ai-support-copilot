<?php

declare(strict_types=1);

namespace App\Application\AnalyseTicket;

use App\Entity\Ticket;
use App\Entity\TicketAnalysis;
use App\services\AiClient;
use Doctrine\ORM\EntityManagerInterface;

final readonly class AnalyseTicket
{
    public function __construct(
        private AiClient $aiClient,
        private EntityManagerInterface $entityManager,
    ) {}

    /**
     * @param string $ticketContent
     * @return AnalyseTicketResult
     */
    public function execute(string $ticketContent): AnalyseTicketResult
    {
        $rawData = $this->aiClient->analyse($ticketContent);
        $result = AnalyseTicketResult::fromArray($rawData);

        $ticket = new Ticket();
        $ticket->setContent($ticketContent);

        $ticketAnalysis = new TicketAnalysis();
        $ticketAnalysis->setTicket($ticket);
        $ticketAnalysis->setSummary($result->summary);
        $ticketAnalysis->setCategory($result->category);
        $ticketAnalysis->setUrgency($result->urgency);
        $ticketAnalysis->setScore($result->score);
        $ticketAnalysis->setSources($result->sources);
        $ticketAnalysis->setCreatedAt(new \DateTime());
        

        $this->entityManager->persist($ticket);
        $this->entityManager->persist($ticketAnalysis);
        $this->entityManager->flush();

        return $result;
    }
}