<template>
	<div v-html="content.description" class="description"></div>
</template>

<script setup lang="ts">
import languageData from "~/assets/language_resource.json";

const selectedLanguage = inject("selectedLanguage");
const content = computed(() => languageData[selectedLanguage.value]);
</script>

<style>
.description {
	margin-bottom: 30px;
	text-align: center;
}
</style>
