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
        <span class="ai-analysis-card__date">{{ formatDate(analysis.createdAt) }}</span>
        <span class="ai-analysis-card__confidence">
          Score : {{ Math.round(analysis.analysis.confidenceScore * 100) }}%
        </span>
      </div>

      <div class="ai-analysis-card__body">
        <div class="ai-analysis-card__tags">
          <span class="tag category">{{ analysis.analysis.category }}</span>
          <span :class="['tag urgency', analysis.analysis.urgency]">{{ analysis.analysis.urgency }}</span>
          <span v-if="analysis.analysis.escalationRequired" class="tag escalation">⚠️ Escalade requise</span>
        </div>

        <p class="ai-analysis-card__summary">
          <strong>Résumé :</strong> {{ analysis.analysis.text }}
        </p>

        <div v-if="analysis.analysis.recommendedPolicy" class="ai-analysis-card__policy">
          <strong>Politique :</strong> <code>{{ analysis.analysis.recommendedPolicy }}</code>
        </div>

        <div v-if="analysis.analysis.justification" class="ai-analysis-card__justification">
          <strong>Raisonnement :</strong> {{ analysis.analysis.justification }}
        </div>
      </div>

      <div
        v-if="analysis.sources?.length"
        class="ai-analysis-card__sources"
      >
        <h4>📚 Sources documentaires</h4>
        <ul>
          <li v-for="source in analysis.sources" :key="source.reference" :title="source.excerpt">
            {{ source.title }} (Score: {{ Math.round(source.score * 100) }}%)
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

        <div
          v-if="feedbacks[analysis.id]?.length"
          class="ai-analysis-card__feedbacks"
        >
          <h4>Avis humains</h4>

          <ul>
            <li v-for="fb in feedbacks[analysis.id]" :key="fb.id">
              <strong>
                {{ fb.decision === 'approved' ? '👍' : '👎' }}
              </strong>
              <span>{{ formatDate(fb.createdAt) }}</span>
              <p v-if="fb.comment">{{ fb.comment }}</p>
            </li>
          </ul>
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
const feedbacks = ref({})
const feedbacksLoading = ref({})

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

/**
 * Send feedback
 */
async function sendFeedback(analysisId, decision) {
  if (submitted.value[analysisId]) {
    return
  }

  submitting.value[analysisId] = true

  await loadFeedbacks(analysisId)

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
 * Load feedbacks for an analysis
 */
async function loadFeedbacks(analysisId) {
  feedbacksLoading.value[analysisId] = true

  try {
    const response = await fetch(
      `/api/ai-analyses/${analysisId}/feedbacks`,
      { headers: { Accept: 'application/json' } }
    )

    if (!response.ok) {
      throw new Error('Feedbacks API error')
    }

    const data = await response.json()
    feedbacks.value[analysisId] = data.feedbacks ?? []
  } catch (e) {
    console.error('[AI Feedbacks]', e)
    feedbacks.value[analysisId] = []
  } finally {
    feedbacksLoading.value[analysisId] = false
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
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.ai-analysis-card__body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.ai-analysis-card__tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: uppercase;
  font-weight: 600;
}

.tag.category { background: #e0f2fe; color: #0369a1; }
.tag.urgency.low { background: #f0fdf4; color: #15803d; }
.tag.urgency.medium { background: #fffbeb; color: #b45309; }
.tag.urgency.high { background: #fef2f2; color: #b91c1c; }
.tag.escalation { background: #fff7ed; color: #c2410c; border: 1px solid #fdba74; }

.ai-analysis-card__summary {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #1f2937;
}

.ai-analysis-card__policy code {
  background: #f3f4f6;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.85rem;
}

.ai-analysis-card__justification {
  font-size: 0.85rem;
  color: #4b5563;
  font-style: italic;
  padding-left: 0.75rem;
  border-left: 2px solid #e5e7eb;
}

.ai-analysis-card__sources {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px dashed #e5e7eb;
}

.ai-analysis-card__sources h4 {
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  color: #374151;
}

.ai-analysis-card__sources ul {
  font-size: 0.8rem;
  color: #6b7280;
  padding-left: 1.25rem;
}

.ai-analysis-card__feedback {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.ai-analysis-card__actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.ai-analysis-card__feedback button {
  font-size: 0.85rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.ai-analysis-card__feedback button:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.ai-analysis-card__feedback button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ai-analysis-card__feedback-status {
  font-size: 0.85rem;
  color: #059669;
  font-weight: 500;
}

.ai-analysis-card__comment {
  width: 100%;
  padding: 0.75rem;
  font-size: 0.85rem;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  resize: vertical;
}

.ai-analysis-card__feedbacks {
  margin-top: 1rem;
  background: #f9fafb;
  padding: 0.75rem;
  border-radius: 8px;
}

.ai-analysis-card__feedbacks h4 {
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  color: #4b5563;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.ai-analysis-card__feedbacks ul {
  list-style: none;
  padding: 0;
}

.ai-analysis-card__feedbacks li {
  font-size: 0.85rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #edf2f7;
}

.ai-analysis-card__feedbacks li:last-child {
  border-bottom: none;
}

</style>
