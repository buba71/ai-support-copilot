<?php

declare(strict_types=1);

namespace App\services;

use Symfony\Contracts\HttpClient\HttpClientInterface;
use Symfony\Contracts\HttpClient\Exception\TransportExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\ClientExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\ServerExceptionInterface;

# This service is used to interact with the API endpoint of the python AI service
final readonly class AiClient
{
    public function __construct(
        private HttpClientInterface $httpClient,
        private string $aiEndpoint,
    ) {}

    /**
    * Sends text to the AI service for analysis and returns the response.
    * @param string $text The text to be analyzed.
    * @return string The analysis result from the AI service.
    * @throws \RuntimeException if there is an error communicating with the AI service.
    */
   public function analyse(string $ticket): array
   {
        try {
            $response = $this->httpClient->request(
                method: 'POST',
                url: $this->aiEndpoint,
                options: [
                    'json' => [
                        'ticket' => $ticket
                    ],
                    'timeout' => 10,
                ]
            );

            return $response->toArray();

        } catch (
            TransportExceptionInterface |
            ClientExceptionInterface |
            ServerExceptionInterface $e) {
            // Log the exception or handle it as needed
            throw new \RuntimeException(
                message: 'Error communicating with AI service: ' . $e->getMessage(),
                previous: $e
            );
        }
   }
}
