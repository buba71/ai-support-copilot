<?php

declare(strict_types=1);

namespace App\Controller;

use App\Application\AnalyseTicket\AnalyseTicket;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attributes\Route;

final class AnalyseTicketController extends AbstractController
{
    #[Route('/api/ticket/analyse', name: 'analyse_ticket', methods: ['POST'])]
    public function __invoke(
      Request $request,
      AnalyseTicket $analyseTicket
      ): JsonResponse {

        $content = $request->toArray()['ticket'??''];
        $result = $analyseTicket->execute($content);

        return $this->json([
            'summary' => $result->summary,
            'category' => $result->category,
            'urgency' => $result->urgency,
            'sources' => $result->sources,
        ]);
    }
}