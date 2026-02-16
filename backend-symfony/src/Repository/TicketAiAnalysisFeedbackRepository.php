<?php

namespace App\Repository;

use App\Entity\TicketAiAnalysisFeedback;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<TicketAiAnalysisFeedback>
 *
 * @method TicketAiAnalysisFeedback|null find($id, $lockMode = null, $lockVersion = null)
 * @method TicketAiAnalysisFeedback|null findOneBy(array $criteria, array $orderBy = null)
 * @method TicketAiAnalysisFeedback[]    findAll()
 * @method TicketAiAnalysisFeedback[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class TicketAiAnalysisFeedbackRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, TicketAiAnalysisFeedback::class);
    }
}
