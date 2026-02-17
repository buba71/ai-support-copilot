<template>
  <section class="ai-analyses">
    <header class="ai-analyses__header">
      <h2>Analyse IA</h2>
      <p class="ai-analyses__disclaimer">
        Aide à la décision — jamais appliquée automatiquement
      </p>
    </header>

    <!-- Loading -->

    <p v-if="loading" class="ai-analyses__state">
      Chargement de l’analyse IA…
    </p>

    <!-- Error -->
    <p v-else-if="error" class="ai-analyses__state error">
      Impossible de charger l’analyse IA.
    </p>

    <!-- Analyses -->
    <article
      v-else
      v-for="analysis in analyses"
      :key="analysis.id"
      class="ai-analysis-card"
    >
      <div class="ai-analysis-card__meta">
        <span>{{ formatDate(analysis.createdAt) }}</span>
        <span>
          Confiance : {{ analysis.analysis.confidenceScore }}
        </span>
      </div>

      <p class="ai-analysis-card__content">
        {{ analysis.analysis.text }}
      </p>

      <div
        v-if="analysis.sources?.length"
        class="ai-analysis-card__sources"
      >
        <h4>Sources utilisées</h4>
        <ul>
          <li v-for="source in analysis.sources" :key="source.reference">
            {{ source.title }}
          </li>
        </ul>
      </div>
      
      <div class="ai-analysis-card__feedback">
        <div>
          <textarea
            v-if="!submitted[analysis.id]"
            v-model="comments[analysis.id]"
            class="ai-analysis-card__comment"
            placeholder="Commentaire optionnel…"
          ></textarea>
        </div>
        <div class="ai-analysis-card__actions">
          <button
            @click="sendFeedback(analysis.id, 'approved')"
            :disabled="submitting[analysis.id] || submitted[analysis.id]"
          >
            👍 Analyse pertinente
          </button>
        
          <button
            @click="sendFeedback(analysis.id, 'rejected')"
            :disabled="submitting[analysis.id] || submitted[analysis.id]"
          >
            👎 Analyse non pertinente
          </button>
        
          <p
            v-if="submitted[analysis.id]"
            class="ai-analysis-card__feedback-status"
          >
            Feedback envoyé
          </p>

          
        </div>
        
      </div>

    </article>

    <!-- Empty -->
    <p
      v-if="!loading && !error && analyses.length === 0"
      class="ai-analyses__state"
    >
      Aucune analyse IA disponible pour ce ticket.
    </p>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

/**
 * Props (Symfony UX Vue)
 */
const props = defineProps({
  ticketId: {
    type: Number,
    required: true,
  },
})

/**
 * State
 */
const analyses = ref([])
const loading = ref(true)
const error = ref(false)
const submitting = ref({})
const submitted = ref({})
const comments = ref({})

/**
 * Lifecycle
 */
onMounted(async () => {

  try {
    const url = `/api/tickets/${props.ticketId}/ai-analyses`;    
    const response = await fetch(
      url,
      {
        headers: { Accept: 'application/json' },
      }
    );
    
    if (!response.ok) {
      throw new Error('API error');
    }

    const data = await response.json();
    analyses.value = data.aiAnalyses ?? []
    
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
})

async function sendFeedback(analysisId, decision) {
  if (submitted.value[analysisId]) {
    return
  }

  submitting.value[analysisId] = true

  try {
    const response = await fetch(
      `/api/ai-analyses/${analysisId}/feedback`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          decision,
          comment: comments.value[analysisId] ?? null
        }),
      }
    )

    if (!response.ok) {
      throw new Error('Feedback API error')
    }

    submitted.value[analysisId] = true

  } catch (e) {

    console.error('[AI Feedback]', e)
    alert('Erreur lors de l’envoi du feedback')

  } finally {
    submitting.value[analysisId] = false
  }
}

/**
 * Helpers
 */
function formatDate(isoDate) {
  return new Date(isoDate).toLocaleString()
}
</script>

<style scoped>
.ai-analyses {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #fafafa;
  border-radius: 12px;
}

.ai-analyses__header {
  margin-bottom: 1rem;
}

.ai-analyses__disclaimer {
  font-size: 0.85rem;
  color: #666;
}

.ai-analyses__state {
  font-size: 0.9rem;
  color: #777;
  padding: 1rem 0;
}

.ai-analyses__state.error {
  color: #a33;
}

.ai-analysis-card {
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.ai-analysis-card__meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #666;
}

.ai-analysis-card__content {
  margin: 1rem 0;
  font-size: 0.95rem;
}

.ai-analysis-card__sources {
  font-size: 0.85rem;
  color: #555;
}

.ai-analysis-card__feedback {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.ai-analysis-card__feedback button {
  font-size: 0.8rem;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  cursor: pointer;
}

.ai-analysis-card__feedback button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ai-analysis-card__feedback-status {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #4a7;
}
.ai-analysis-card__comment {
  width: 70%;
  margin-top: 0.5rem;
  padding: 0.5rem;
  font-size: 0.85rem;
  border-radius: 6px;
  border: 1px solid #ddd;
  resize: vertical;
}
</style>
