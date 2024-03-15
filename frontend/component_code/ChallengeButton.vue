<template>
	<button @click="scrollIntoMessageSubmit">{{ content.challenge }}</button>
</template>

<script setup lang="ts">
import { inject, computed } from "vue";
import languageData from "~/assets/language_resource.json";

const selectedLanguage = inject("selectedLanguage");
const content = computed(() => languageData[selectedLanguage.value]);

function scrollIntoMessageSubmit() {
	const element = document.querySelector(".chat-container");
	if (element) {
		element.scrollIntoView({ behavior: "smooth", block: "center" });
	}
}
</script>

<style>
button {
	padding: 10px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
}
</style>
