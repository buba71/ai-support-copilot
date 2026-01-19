<?php

declare(strict_types=1);

namespace App\Application\AnalyseTicket;

use App\services\AiClient;

final readonly class AnalyseTicket
{
    public function __construct(
        private AiClient $aiClient,
    ) {}

    public function execute(string $ticketContent): AnalyseTicketResult
    {
        $result = $this->aiClient->analyse($ticketContent);

        return AnalyseTicketResult::fromArray($result);
    }
}