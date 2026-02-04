<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Ticket;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;


class TicketController extends AbstractController
{
  #[Route('/ticket/{id}', name: 'ticket_show', methods: ['GET'])]
  public function show(Ticket $ticket): Response
  {
    // (Optionnel mais courant)
    // $this->denyAccessUnlessGranted('VIEW', $ticket);
    return $this->render('ticket/show.html.twig', [
        'ticket' => $ticket,
    ]);
  }
}