<?php

declare(strict_types=1);

namespace App\Application\AnalyseTicket;

final class AnalyseTicketResult
{
    private function __construct(
        public readonly string $summary,
        public readonly string $category,
        public readonly string $urgency,
        public readonly array $sources,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            summary:  $data['summary'] ?? '',
            category: $data['category'] ?? '',
            urgency:  $data['urgency'] ?? '',
            sources:  $data['sources'] ?? [],
        );
    }
}