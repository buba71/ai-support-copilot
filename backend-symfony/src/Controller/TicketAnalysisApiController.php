<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Ticket;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;

final class TicketAnalysisApiController extends AbstractController
{
    #[Route('/api/tickets/{id}/ai-analyses', name: 'api_ticket_analyses', methods: ['GET'])]
    public function __invoke(Ticket $ticket): JsonResponse
    {
        $analyses = $ticket->getTicketAnalysis();
        
        $data = [];
        foreach ($analyses as $analysis) {
            $data[] = [
                'id' => $analysis->getId(),
                'createdAt' => $analysis->getCreatedAt()?->format(\DateTimeInterface::ATOM),
                'analysis' => [
                    'text' => $analysis->getSummary(),
                    'confidenceScore' => $analysis->getScore(),
                ],
                'sources' => array_map(function($source) {
                    // Adapt source format if needed. 
                    // Based on Vue component: :key="source.reference" {{ source.title }}
                    // Based on Python engine: "source", "score", "excerpt"
                    return [
                        'reference' => $source['source'] ?? 'ref',
                        'title' => $source['source'] ?? 'Source',
                        'excerpt' => $source['excerpt'] ?? '',
                        'score' => $source['score'] ?? 0,
                    ];
                }, $analysis->getSources()),
            ];
        }

        return $this->json([
            'aiAnalyses' => $data,
        ]);
    }
}
