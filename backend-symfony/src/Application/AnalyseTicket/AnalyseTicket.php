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
     * @return array
     */
    public function start(string $ticketContent): array
    {
        return $this->aiClient->startAnalysis($ticketContent);
    }

    /**
     * Fetches the job result from the AI service and persists it if finished.
     * 
     * @param string $jobId
     * @param string $ticketContent
     * @return AnalyseTicketResult
     */
    public function fetchJobAndPersistIfFinished(string $jobId, string $ticketContent): array
    {
        $jobData = $this->aiClient->getJob($jobId);
        
        if (($jobData['status'] ?? null) !== 'finished') {
            return $jobData;
        }

        $resultData = $jobData['result'] ?? [];
        

        $result = AnalyseTicketResult::fromArray($resultData);

        $this->persistAnalysis($ticketContent, $result);

        return $jobData;
    }

    private function persistAnalysis(string $ticketContent, AnalyseTicketResult $result): void
    {
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
        
        // New fields
        $ticketAnalysis->setRecommendedPolicy($result->recommendedPolicy);
        $ticketAnalysis->setEscalationRequired($result->escalationRequired);
        $ticketAnalysis->setJustification($result->justification);
        $ticketAnalysis->setMetadata($result->meta);

        $this->entityManager->persist($ticket);
        $this->entityManager->persist($ticketAnalysis);
        $this->entityManager->flush();
    }
}