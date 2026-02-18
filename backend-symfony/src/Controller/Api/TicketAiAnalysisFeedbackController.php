<?php

declare(strict_types=1);

namespace App\Controller\Api;

use App\Entity\TicketAnalysis;
use App\Entity\TicketAiAnalysisFeedback;
use App\Enum\AiFeedbackDecision;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/ai-analyses')]
final class TicketAiAnalysisFeedbackController extends AbstractController
{
    #[Route('/{id}/feedback', name: 'api_ticket_ai_analysis_feedback_create', methods: ['POST'])]
    public function create(
        TicketAnalysis $analysis,
        Request $request,
        EntityManagerInterface $entityManager
    ): Response {
        $payload = json_decode($request->getContent(), true);

        if (!\is_array($payload)) {
            return $this->json(['error' => 'Invalid JSON body'], Response::HTTP_BAD_REQUEST);
        }

        $decision = AiFeedbackDecision::tryFrom($payload['decision'] ?? '');

        if ($decision === null) {
            return $this->json(['error' => 'Invalid decision'], Response::HTTP_BAD_REQUEST);
        }

        $feedback = new TicketAiAnalysisFeedback(
            $analysis,
            $decision,
            $payload['comment'] ?? null
        );

        $entityManager->persist($feedback);
        $entityManager->flush();

        return $this->json(null, Response::HTTP_CREATED);
    }

    #[Route('/{id}/feedbacks', name: 'api_ticket_ai_analysis_feedback_get', methods: ['GET'])]
    public function getFeedbacks(
        TicketAnalysis $analysis
    ): JsonResponse {

        $feedbacks = $analysis->getFeedbacks();

        $response = $this->json([
            'analysisId' => $analysis->getId(),
            'feedbacks'  => array_map(fn(TicketAiAnalysisFeedback $fb) => [
                'id' => $fb->getId(),
                'decision' => $fb->getDecision()->value,
                'comment' => $fb->getComment(),
                'createdAt' => $fb->getCreatedAt()->format('Y-m-d H:i:s'),
            ], $feedbacks->toArray())
        ]);

        return $response;
    }
}



    

