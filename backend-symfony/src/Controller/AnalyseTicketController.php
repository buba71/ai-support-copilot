<?php

declare(strict_types=1);

namespace App\Controller;

use App\Application\AnalyseTicket\AnalyseTicket;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;

final class AnalyseTicketController extends AbstractController
{
    #[Route('/api/ticket/analyse', name: 'analyse_ticket', methods: ['POST'])]
    public function __invoke(
      Request $request,
      AnalyseTicket $analyseTicket
      ): JsonResponse {
        try {
            $data = $request->toArray();
            $content = $data['ticket'] ?? '';

            if (empty($content)) {
                return $this->json(['error' => 'Le contenu du ticket ne peut pas être vide'], 400);
            }
            
            $rawData = $analyseTicket->getRawAnalysis($content);

            return $this->json($rawData);
        } catch (\RuntimeException $e) {
            return $this->json(['error' => $e->getMessage()], 500);
        } catch (\Exception $e) {
            return $this->json(['error' => 'Une erreur est survenue lors de l\'analyse du ticket'], 500);
        }
    }
}