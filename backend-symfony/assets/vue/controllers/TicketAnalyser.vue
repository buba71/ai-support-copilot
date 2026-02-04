<template>
  <div class="ticket-analyser">
    <textarea
      v-model="ticket"
      placeholder="Colle le ticket client ici…"
      class="ticket-input"
      rows="4"
    />

    <button
      @click="analyzeTicket"
      class="analyze-button"
      :disabled="loading"
    >
      {{ loading ? 'Analyse en cours…' : 'Analyser le ticket' }}
    </button>

    <p v-if="error" class="error-message">{{ error }}</p>

    <div v-if="result" class="result-box">
      <p><strong>Résumé :</strong> {{ result.summary }}</p>
      <p><strong>Catégorie :</strong> {{ result.category }}</p>
      <p><strong>Urgence :</strong> {{ result.urgency }}</p>

      <div v-if="result.sources?.length">
        <h4 class="sources-title">Sources utilisées :</h4>
        <ul class="sources-list">
          <li v-for="(src, i) in result.sources" :key="i">
            {{ src }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'

const ticket = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref(null)

const analyzeTicket = async () => {
  loading.value = true
  error.value = null
  result.value = null

  try {
    const response = await fetch('/api/ticket/analyse', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ticket: ticket.value })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Erreur lors de l\'analyse' }))
      throw new Error(errorData.error || `Erreur HTTP: ${response.status}`)
    }

    result.value = await response.json()

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
  gap: 16px;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.ticket-input {
  width: 100%;
  border: 1px solid #ccc;
  padding: 8px;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
}

.analyze-button {
  background-color: #2563eb;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.2s;
}

.analyze-button:hover:not(:disabled) {
  background-color: #1d4ed8;
}

.analyze-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  padding: 10px;
  background-color: #fee2e2;
  border-radius: 4px;
  border: 1px solid #fca5a5;
}

.result-box {
  border: 1px solid #e5e7eb;
  padding: 16px;
  border-radius: 4px;
  background-color: #f9fafb;
}

.result-box p {
  margin: 8px 0;
}

.sources-title {
  margin-top: 16px;
  font-weight: 600;
  font-size: 16px;
}

.sources-list {
  list-style-type: disc;
  margin-left: 20px;
  margin-top: 8px;
}

.sources-list li {
  margin: 4px 0;
}
</style>
