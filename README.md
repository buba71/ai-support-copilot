# AI Support Copilot

Application d'analyse de tickets client utilisant l'IA pour fournir des réponses automatisées. Le projet est composé d'un backend Symfony qui expose une interface web Vue.js et communique avec un service d'IA Python basé sur FastAPI.

## 🏗️ Architecture

Le projet est composé de deux parties principales :

- **backend-symfony** : Application Symfony 7.4 avec Vue.js 3 pour l'interface utilisateur
- **ai-engine** : Service FastAPI (Python) pour l'analyse de tickets avec RAG (Retrieval-Augmented Generation)

## 📋 Prérequis

### Backend Symfony
- PHP >= 8.2
- Composer
- Node.js >= 18.x et npm
- Symfony CLI (optionnel mais recommandé)

### AI Engine
- Python >= 3.10
- pip

## 🚀 Installation

### 1. Installation du Backend Symfony

```bash
cd backend-symfony

# Installer les dépendances PHP
composer install

# Installer les dépendances Node.js
npm install

# Compiler les assets
npm run build
```

### 2. Configuration du Backend

Créez un fichier `.env.local` dans `backend-symfony/` si nécessaire :

```env
# Configuration de l'endpoint du service IA
# Par défaut : http://localhost:8000/analyze-ticket
# Modifiable dans config/services.yaml
```

### 3. Installation du Service IA

```bash
cd ai-engine

# Créer un environnement virtuel Python
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac :
source venv/bin/activate
# Sur Windows :
# venv\Scripts\activate

# Installer les dépendances Python
pip install fastapi uvicorn
# Installer les autres dépendances nécessaires (selon vos besoins)
```

## ▶️ Démarrage de l'application

### 1. Démarrer le service IA (Terminal 1)

```bash
cd ai-engine
source venv/bin/activate  # Si pas déjà activé
uvicorn api.main:app --reload --port 8000
```

Le service IA sera accessible sur `http://localhost:8000`

### 2. Démarrer le serveur Symfony (Terminal 2)

```bash
cd backend-symfony

# Option 1 : Utiliser le serveur Symfony CLI
symfony server:start

# Option 2 : Utiliser le serveur PHP intégré
php -S localhost:8001 -t public
```

L'application sera accessible sur `http://localhost:8001` (ou le port configuré par Symfony CLI)

### 3. Compiler les assets en mode développement (Terminal 3 - Optionnel)

Si vous modifiez les composants Vue.js, lancez le mode watch :

```bash
cd backend-symfony
npm run watch
```

## 🧪 Procédure de test

### Test 1 : Vérifier que les services sont démarrés

#### Vérifier le service IA
```bash
curl http://localhost:8000/docs
```
Vous devriez voir la documentation interactive de l'API FastAPI.

#### Vérifier le backend Symfony
```bash
curl http://localhost:8001
```
Vous devriez voir la page d'accueil.

### Test 2 : Tester l'API directement

#### Test du service IA Python

```bash
curl -X POST http://localhost:8000/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket": "Mon colis n\'est pas arrivé et la commande est en retard"}'
```

Réponse attendue :
```json
{
  "summary": "...",
  "category": "...",
  "urgency": "...",
  "sources": [...]
}
```

#### Test du backend Symfony

```bash
curl -X POST http://localhost:8001/api/ticket/analyse \
  -H "Content-Type: application/json" \
  -d '{"ticket": "Mon colis n\'est pas arrivé et la commande est en retard"}'
```

Réponse attendue :
```json
{
  "summary": "...",
  "category": "...",
  "urgency": "...",
  "sources": [...]
}
```

### Test 3 : Test de l'interface utilisateur

1. **Accéder à l'application** : Ouvrez votre navigateur sur `http://localhost:8001`

2. **Tester le composant Vue.js** :
   - Vous devriez voir une zone de texte "Colle le ticket client ici…"
   - Saisissez un exemple de ticket client, par exemple :
     ```
     Bonjour, j'ai commandé un produit la semaine dernière mais je ne l'ai toujours pas reçu. 
     Le statut de ma commande indique "expédié" depuis 5 jours. Pouvez-vous m'aider ?
     ```
   - Cliquez sur le bouton "Analyser le ticket"
   - Vous devriez voir apparaître :
     - Un résumé du ticket
     - Une catégorie
     - Un niveau d'urgence
     - Les sources utilisées (si disponibles)

3. **Vérifier la console du navigateur** (F12) :
   - Ouvrez l'onglet "Console"
   - Vérifiez qu'il n'y a pas d'erreurs JavaScript
   - Vous devriez voir les messages de débogage :
     - "Vérification des composants Vue enregistrés..."
     - "Composant Hello trouvé: ..."
     - "Composant TicketAnalyser trouvé: ..."

### Test 4 : Test des erreurs

#### Test avec un ticket vide
- Laissez la zone de texte vide
- Cliquez sur "Analyser le ticket"
- Vous devriez voir un message d'erreur : "Le contenu du ticket ne peut pas être vide"

#### Test avec le service IA arrêté
1. Arrêtez le service IA (Ctrl+C dans le terminal 1)
2. Essayez d'analyser un ticket
3. Vous devriez voir un message d'erreur indiquant que le service IA n'est pas accessible

### Test 5 : Vérification des routes Symfony

```bash
cd backend-symfony
php bin/console debug:router
```

Vous devriez voir :
- `app_home` : Route GET `/` pour la page d'accueil
- `analyse_ticket` : Route POST `/api/ticket/analyse` pour l'analyse de ticket

### Test 6 : Vérification de la compilation des assets

```bash
cd backend-symfony
npm run build
```

Vérifiez qu'il n'y a pas d'erreurs et que les fichiers sont générés dans `public/build/` :
- `app.js`
- `app.css`
- Fichiers de chunks Vue.js

## 🔧 Dépannage

### Le composant Vue ne s'affiche pas
1. Vérifiez que les assets sont compilés : `npm run build`
2. Vérifiez la console du navigateur pour les erreurs JavaScript
3. Vérifiez que `window.resolveVueComponent` est défini dans la console

### L'API retourne une erreur 500
1. Vérifiez que le service IA est démarré sur le port 8000
2. Vérifiez la configuration dans `backend-symfony/config/services.yaml`
3. Consultez les logs Symfony : `var/log/dev.log`

### La route n'est pas trouvée
1. Videz le cache : `php bin/console cache:clear`
2. Vérifiez que l'attribut `#[Route]` utilise `Attribute\Route` et non `Attributes\Route`

### Erreur de namespace PHP
- Vérifiez que les namespaces correspondent entre les fichiers
- Exécutez : `composer dump-autoload`

## 📁 Structure du projet

```
ai-support-copilot/
├── backend-symfony/          # Application Symfony
│   ├── assets/
│   │   ├── vue/
│   │   │   └── controllers/
│   │   │       ├── TicketAnalyser.vue   # Composant Vue principal
│   │   │       └── Hello.vue            # Composant de test
│   │   ├── app.js            # Point d'entrée JavaScript
│   │   └── styles/
│   ├── config/
│   │   └── services.yaml     # Configuration des services
│   ├── public/
│   │   └── build/            # Assets compilés
│   ├── src/
│   │   ├── Controller/
│   │   │   ├── HomeController.php
│   │   │   └── AnalyseTicketController.php
│   │   ├── Application/
│   │   │   └── AnalyseTicket/
│   │   │       ├── AnalyseTicket.php
│   │   │       └── AnalyseTicketResult.php
│   │   └── services/
│   │       └── AiClient.php  # Client HTTP pour le service IA
│   └── templates/
│       ├── base.html.twig
│       └── home/
│           └── index.html.twig
│
└── ai-engine/                # Service IA Python
    ├── api/                  # Endpoints FastAPI
    ├── ai_service/           # Logique orchestration IA
    │   ├── guardrails/       # Moteur de règles de sécurité
    │   ├── monitoring/       # Tracking tokens, coûts, latence
    │   ├── prompts.py        # Templates de prompts versionnés
    │   └── ticket_analyser.py
    └── rag_docs/             # Base de connaissances (PDF/Markdown)
```

## 🔌 Points d'API

### Backend Symfony

- `GET /` : Page d'accueil avec l'interface d'analyse
- `POST /api/ticket/analyse` : Analyse un ticket client
  - Body : `{ "ticket": "contenu du ticket" }`
  - Response : `{ "decision": {...}, "meta": {...} }`

### Service IA (FastAPI)

- `POST /analyze-ticket` : Analyse un ticket avec l'IA
  - Body : `{ "ticket": "contenu du ticket" }`
  - Response : `{ "decision": {...}, "meta": {...} }` (Inclus résumé, catégorie, urgence, sources RAG et métadonnées de monitoring)

## 🛠️ Commandes utiles

### Backend Symfony

```bash
# Installer les dépendances
composer install
npm install

# Compiler les assets
npm run build           # Production
npm run dev            # Développement
npm run watch          # Mode watch

# Cache
php bin/console cache:clear

# Routes
php bin/console debug:router

# Serveur
symfony server:start
# ou
php -S localhost:8001 -t public
```

### AI Engine

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Démarrer le serveur
uvicorn api.main:app --reload --port 8000
```

## 🛡️ Observability & Guardrails

L'**AI Engine** intègre une couche robuste de monitoring et de sécurité pour garantir la fiabilité des analyses :

- **Decision / Meta separation** : Chaque réponse de l'API est structurée en deux blocs distincts :
  - `decision` : Contient les données métier validées par Pydantic (`summary`, `category`, `urgency`, `recommended_policy`, `escalation_required`, `justification`).
  - `meta` : Regroupe les métadonnées techniques (`model`, `prompt_version`, `latency_ms`, `tokens_input`, `tokens_output`, `estimated_cost`, `guardrail_triggered`).
- **Prompt versioning** : Versionnement strict via la variable `AI_PROMPT_VERSION` (actuellement `2.0_decision_engine`). Chaque analyse est tracée avec la version exacte du prompt utilisée, permettant un suivi précis des évolutions de performance.
- **Guardrail engine** : Un moteur de règles déterministes (`GuardrailEngine`) intervient en post-traitement pour corriger les hallucinations ou erreurs de logique de l'IA :
  - **GR-001** : Force `escalation_required` à `true` si l'urgence est `high`.
  - **GR-002** : Détection de mots-clés juridiques pour forcer l'escalade manuelle.
  - **GR-003** : Interdit l'utilisation de la politique FAQ pour les cas critiques, redirigeant vers une procédure d'escalade.
- **Token & cost tracking** : Calcul en temps réel basé sur les tarifs du modèle (ex: `$0.15/1M` tokens en entrée, `$0.60/1M` en sortie pour `gpt-4o-mini`).
- **Latency measurement** : Mesure précise de la latence de bout en bout (orchestration LLM + recherche RAG) renvoyée en millisecondes.
- **Evaluation Metrics** : Le projet inclut un système d'évaluation (`EvaluationMetrics`) pour calculer la précision des politiques recommandées, le taux d'escalade correct et le taux d'erreur global sur des datasets de test.

## 📝 Notes de développement

- Les composants Vue.js sont compilés avec Webpack Encore
- Le service IA doit être démarré avant le backend Symfony pour que les tests fonctionnent
- La configuration de l'endpoint IA se trouve dans `backend-symfony/config/services.yaml`
- Les styles CSS sont définis directement dans les composants Vue avec `<style scoped>`

## 📄 Licence

Proprietary
