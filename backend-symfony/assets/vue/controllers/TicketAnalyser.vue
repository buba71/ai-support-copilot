<template>
  <div class="ticket-analyser">
    <h3>Analyse IA du ticket</h3>

    <textarea
      v-model="ticket"
      rows="6"
      placeholder="Saisissez le contenu du ticket..."
    />

    <button
      type="button"
      :disabled="loading || !ticket.trim()"
      @click="analyzeTicket"
    >
      {{ loading ? 'Analyse en cours...' : 'Analyser le ticket' }}
    </button>

    <p v-if="jobId" class="job-status">
      Job IA : {{ jobId }}
    </p>

    <p v-if="error" class="error">
      {{ error }}
    </p>

    <div v-if="result" class="result-box">
      <h4>Analyse interne support</h4>

      <p>
        <strong>Résumé :</strong>
        {{ result.internal_analysis?.summary }}
      </p>

      <p>
        <strong>Catégorie :</strong>
        {{ result.internal_analysis?.category }}
      </p>

      <p>
        <strong>Urgence :</strong>
        {{ result.internal_analysis?.urgency }}
      </p>

      <p>
        <strong>Politique recommandée :</strong>
        {{ result.internal_analysis?.recommended_policy }}
      </p>

      <p>
        <strong>Escalade requise :</strong>
        {{ result.internal_analysis?.escalation_required ? 'Oui' : 'Non' }}
      </p>

      <p>
        <strong>Confiance :</strong>
        {{ result.internal_analysis?.confidence_score }}
      </p>

      <p v-if="result.internal_analysis?.fallback_reason">
        <strong>Raison du fallback :</strong>
        {{ result.internal_analysis.fallback_reason }}
      </p>

      <h4>Brouillon de réponse client</h4>

      <p class="draft-reply">
        {{ result.draft_reply }}
      </p>

      <h4>Sources RAG</h4>

      <ul v-if="result.internal_analysis?.used_sources?.length">
        <li
          v-for="(source, index) in result.internal_analysis.used_sources"
          :key="index"
        >
          <strong>{{ source }}</strong>
        </li>
      </ul>

      <p v-else>
        Aucune source disponible.
      </p>

      <details>
        <summary>JSON complet</summary>
        <pre>{{ result }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const ticket = ref('')
const loading = ref(false)
const error = ref(null)
const result = ref(null)
const jobId = ref(null)

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const pollJob = async (id) => {
  for (let attempt = 0; attempt < 30; attempt++) {
    const response = await fetch(`/api/analyse/jobs/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ticket: ticket.value
      })
    })

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ error: 'Erreur lors de la récupération du job' }))

      throw new Error(errorData.error || `Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()

    if (data.status === 'finished') {
      return data.result
    }

    if (data.status === 'failed') {
      throw new Error('Le job IA a échoué')
    }

    await sleep(1000)
  }

  throw new Error('Le job IA n’a pas terminé dans le délai prévu')
}

const analyzeTicket = async () => {
  loading.value = true
  error.value = null
  result.value = null
  jobId.value = null

  try {
    const response = await fetch('/api/ticket/analyse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ticket: ticket.value
      })
    })

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ error: 'Erreur lors de l’analyse' }))

      throw new Error(errorData.error || `Erreur HTTP: ${response.status}`)
    }

    const jobData = await response.json()

    if (!jobData.job_id) {
      throw new Error('Aucun job_id retourné par le serveur')
    }

    jobId.value = jobData.job_id

    const finalResult = await pollJob(jobData.job_id)

    result.value = finalResult.decision || finalResult
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.ticket-analyser {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

textarea {
  width: 100%;
  padding: 0.75rem;
}

button {
  width: fit-content;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.error {
  color: #b00020;
  font-weight: bold;
}

.job-status {
  font-size: 0.9rem;
  opacity: 0.8;
}

.result-box {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.draft-reply {
  white-space: pre-line;
}

pre {
  white-space: pre-wrap;
  overflow-x: auto;
}
</style>