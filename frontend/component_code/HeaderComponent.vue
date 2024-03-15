<template>
	<h1>{{ content.title }}</h1>
</template>

<script setup lang="ts">
import languageData from "~/assets/language_resource.json";

const selectedLanguage = inject("selectedLanguage");
const content = computed(() => languageData[selectedLanguage.value]);
</script>

<style>
h1 {
	font-family: LifeIsbattle;
}
</style>
