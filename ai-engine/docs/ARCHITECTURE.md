# Project Architecture

## Problème produit

Le système vise à assister un support client en :

- analysant automatiquement les tickets
- récupérant du contexte documentaire pertinent
- produisant une réponse structurée et exploitable

Contraintes :
- fiabilité des réponses
- traçabilité (sources)
- coût des appels LLM
- gestion des cas d’incertitude

## Main Flow
Frontend -> Symfony -> FastAPI -> ticket_analyser -> rag_service -> vector_db -> LLM

Frontend / Symfony
-> envoie un ticket au moteur IA

TicketAnalyzer
-> orchestre le pipeline d’analyse
-> demande du contexte au RagService
-> construit le prompt
-> appelle le LLM via LLMClient
-> valide la sortie
-> applique les guardrails
-> enrichit le résultat avec le monitoring

RagService
-> interroge la couche vectorielle
-> transforme les résultats bruts en chunks exploitables

VectorDB
-> stocke les documents et effectue la recherche sémantique via Chroma

LLMClient
-> appelle OpenAI avec retry
-> retourne la réponse et les métadonnées d’usage

## Séparation des couches

### Orchestration
- TicketAnalyzer

Responsabilité :
- coordonner les étapes du pipeline

---

### Retrieval (IA)
- RagService

Responsabilité :
- récupérer et normaliser le contexte

---

### Génération (IA)
- LLMClient

Responsabilité :
- appeler le modèle et gérer les erreurs techniques

---

### Infrastructure
- VectorDB
- Cache

Responsabilité :
- stockage, accès aux données, performance

---

### Fiabilité / Observabilité
- GuardrailEngine
- MonitoringService

Responsabilité :
- rendre le système fiable et mesurable

## Modules

### ticket_analyser
- role: orchestrate the complete analysis of a support ticket
- inputs: ticket text, RAG activation status
- outputs: enriched analysis result with business data, RAG sources and technical metadata
- depends on: llm_client, rag_service, monitoring_service, guardrail_engine, cache_service
- logic type: AI orchestration

Remarque : Le module agit comme orchestrateur principal du pipeline IA, mais son contrat de sortie doit être stabilisé pour éviter des formats différents selon les erreurs.

### Contrat actuel de TicketAnalyzer

Entrée :
- ticket_text: str
- use_rag: bool

Sortie nominale :
- analyse structurée validée par TicketAnalysis
- enrichie avec meta
- enrichie avec rag_documents

Sorties d’erreur actuelles :
- JSON invalide
- schéma invalide

### rag_service
- rôle : interroger le moteur de recherche vectorielle et normaliser les résultats utiles au pipeline IA
- entrées : query texte, nombre de résultats attendu
- sorties : liste de chunks enrichis contenant contenu, source et score
- dépend de : vector_db
- type de logique : IA / retrieval

Remarque :
Le module sert de couche intermédiaire entre la base vectorielle et l’orchestrateur. Il simplifie les résultats bruts, mais son contrat de sortie devra être stabilisé avec un schéma explicite.

## Contrat actuel de RagService

Entrée :
- query: str
- k: int

Sortie actuelle :
- list[dict] avec :
  - content
  - source
  - score

Limites actuelles :
- dépendance directe à VectorDB: corrigée le 08/04/26
- format implicite non typé
- score calculé selon une convention locale

### vector_db
- rôle : stocker les documents vectorisés et permettre une recherche sémantique dans l’index
- entrées : documents à indexer, requête texte, identifiant de document
- sorties : résultats bruts de recherche avec contenu, métadonnées et distance ; booléen pour l’existence d’un document
- dépend de : ChromaDB, fonction d’embedding OpenAI, variables d’environnement
- type de logique : infrastructure

Remarque :
Le module encapsule correctement l’accès à la base vectorielle, mais ses formats d’entrée et de sortie restent implicites et gagneraient à être typés.

### llm_client
- rôle : appeler le fournisseur LLM, gérer le retry technique et renvoyer une réponse simplifiée avec métadonnées utiles
- entrées : messages format chat, température
- sorties : contenu texte de la réponse, tokens d’entrée, tokens de sortie, modèle utilisé
- dépend de : OpenAI SDK, variables d’environnement, RetryService
- type de logique : infrastructure IA

Remarque :
Le module encapsule correctement l’appel au modèle, mais ses paramètres critiques restent hardcodés et son contrat d’entrée/sortie gagnerait à être typé plus explicitement.