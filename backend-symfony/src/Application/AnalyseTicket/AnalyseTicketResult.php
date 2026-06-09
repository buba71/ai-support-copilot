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

        $analysis = $decision['internal_analysis'] ?? $decision;

        $meta = $data['meta'] ?? [];

        $ragDocs = $analysis['rag_documents'] ?? [];

        $avgScore = !empty($ragDocs)
            ? array_sum(array_column($ragDocs, 'score')) / count($ragDocs)
            : 0.0;

        return new self(
            summary:  $analysis['summary'] ?? '',
            category: $analysis['category'] ?? '',
            urgency:  $analysis['urgency'] ?? '',
            sources:  $ragDocs ?: ($analysis['used_sources'] ?? []),
            score:    (float) ($analysis['score'] ?? $analysis['confidence_score'] ?? $avgScore),
            recommendedPolicy: $analysis['recommended_policy'] ?? null,
            escalationRequired: (bool) ($analysis['escalation_required'] ?? false),
            justification: $analysis['justification'] ?? null,
            meta: [
                ...$meta,
                'draft_reply' => $decision['draft_reply'] ?? null,
                'confidence_score' => $analysis['confidence_score'] ?? null,
                'insufficient_context' => $analysis['insufficient_context'] ?? null,
                'fallback_reason' => $analysis['fallback_reason'] ?? null,
                'used_sources' => $analysis['used_sources'] ?? [],
            ],
        );
    }
}