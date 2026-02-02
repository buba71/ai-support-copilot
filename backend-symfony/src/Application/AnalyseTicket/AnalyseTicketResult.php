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
        public readonly float $score,
    ) {}

    public static function fromArray(array $data): self
    {
        $ragDocs = $data['rag_documents'] ?? [];
        $avgScore = !empty($ragDocs) ? array_sum(array_column($ragDocs, 'score')) / count($ragDocs) : 0.0;

        return new self(
            summary:  $data['summary'] ?? '',
            category: $data['category'] ?? '',
            urgency:  $data['urgency'] ?? '',
            sources:  $ragDocs ?: ($data['sources'] ?? []),
            score:    (float) ($data['score'] ?? $avgScore),
        );
    }
}