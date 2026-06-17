<?php

declare(strict_types=1);

namespace App\Controller;

use App\Application\AnalyseTicket\AnalyseTicket;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;
use App\Repository\TicketRepository;

final class AnalyseTicketController extends AbstractController
{
    #[Route('/api/ticket/analyse', name: 'analyse_ticket', methods: ['POST'])]
    public function start(
      Request $request,
      AnalyseTicket $analyseTicket,
      TicketRepository $ticketRepository
      ): JsonResponse {
        try {
            $data = $request->toArray();

            $content = $data['ticket'] ?? null;

            if (!$content && isset($data['ticketId'])) {
                $ticket = $ticketRepository->find((int) $data['ticketId']);

                if (!$ticket) {
                    return $this->json(['error' => 'Ticket introuvable'], 404);
                }

                $content = $ticket->getContent(); // adapte si ton getter a un autre nom
            }

            if (!$content) {
                return $this->json([
                    'error' => 'Le contenu du ticket ne peut pas être vide'
                ], 400);
            }
            
            $rawData = $analyseTicket->start($content);

            return $this->json($rawData);
        } catch (\RuntimeException $e) {
            return $this->json(['error' => $e->getMessage()], 500);
        } catch (\Exception $e) {
            return $this->json(['error' => 'Une erreur est survenue lors de l\'analyse du ticket'], 500);
        }
    }

    #[Route('/api/analyse/jobs/{jobId}', name: 'analyse_ticket_job', methods: ['POST'])]
    public function job(
        string $jobId,
        Request $request,
        AnalyseTicket $analyseTicket,
        TicketRepository $ticketRepository
    ): JsonResponse {

        try {
            $data = $request->toArray();
            $content = $data['ticket'] ?? null;

            if (!$content && isset($data['ticketId'])) {
                $ticket = $ticketRepository->find((int) $data['ticketId']);

                if (!$ticket) {
                    return $this->json(['error' => 'Ticket introuvable'], 404);
                }

                $content = $ticket->getContent(); // adapte si ton getter a un autre nom
            }

            if (!$content) {
                return $this->json([
                    'error' => 'Le contenu du ticket ne peut pas être vide'
                ], 400);
            }
            
            $jobData = $analyseTicket->fetchJobAndPersistIfFinished(
                jobId: $jobId,
                ticketContent: $content
            );

            return $this->json($jobData);

        } catch (\RuntimeException $e) {
            return $this->json(['error' => $e->getMessage()], 500);
        } catch (\Exception $e) {
            return $this->json(['error' => 'Une erreur est survenue lors de la récupération du job IA',], 500);
        }
    }
}