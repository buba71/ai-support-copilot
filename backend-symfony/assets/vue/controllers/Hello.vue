<template>
    <div class="vue-component">
        <h2 class="title">Bonjour depuis Vue 3 ! (SFC) 🚀</h2>
        <p>Bonjour <strong>{{ name }}</strong>, ce composant est compilé par Webpack Encore !</p>
        <button @click="count++" class="btn">
            Compteur : {{ count }}
        </button>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    name: String
});

const count = ref(0);
</script>

<style scoped>
.vue-component {
    padding: 20px;
    border: 2px solid #42b983;
    border-radius: 8px;
    background-color: #f0fdf4;
    color: #166534;
    font-family: 'Inter', sans-serif;
}

.title {
    color: #42b983;
    margin-top: 0;
}

.btn {
    padding: 8px 16px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.btn:hover {
    background-color: #3aa876;
}
</style>
