<?php

declare(strict_types=1);

namespace App\Enum;

enum AiFeedbackDecision: string
{
    case APPROVED = 'approved';
    case REJECTED = 'rejected';
}