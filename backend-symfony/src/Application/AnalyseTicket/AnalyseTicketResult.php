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
        public readonly ?string $recommendedPolicy = null,
        public readonly bool $escalationRequired = false,
        public readonly ?string $justification = null,
        public readonly array $meta = [],
    ) {}

    public static function fromArray(array $data): self
    {
        $decision = $data['decision'] ?? [];
        $meta = $data['meta'] ?? [];
        
        $ragDocs = $decision['rag_documents'] ?? [];
        $avgScore = !empty($ragDocs) ? array_sum(array_column($ragDocs, 'score')) / count($ragDocs) : 0.0;

        return new self(
            summary:  $decision['summary'] ?? '',
            category: $decision['category'] ?? '',
            urgency:  $decision['urgency'] ?? '',
            sources:  $ragDocs ?: ($decision['sources'] ?? []),
            score:    (float) ($decision['score'] ?? $avgScore),
            recommendedPolicy: $decision['recommended_policy'] ?? null,
            escalationRequired: (bool) ($decision['escalation_required'] ?? false),
            justification: $decision['justification'] ?? null,
            meta: $meta,
        );
    }
}