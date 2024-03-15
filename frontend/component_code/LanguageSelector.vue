<template>
	<div class="select-language">
		<div
			:class="{ selected: selectedLanguage === 'EN' }"
			@click="selectLanguage('EN')"
		>
			english
		</div>
		<div
			:class="{ selected: selectedLanguage === 'KO' }"
			@click="selectLanguage('KO')"
		>
			korean
		</div>
	</div>
</template>

<script setup lang="ts">
const selectedLanguage = ref("EN");

const emit = defineEmits(["languageChanged"]);

function selectLanguage(language) {
	selectedLanguage.value = language;
	emit("languageChanged", language);
}
</script>

<style>
.select-language div {
	display: inline-block;
	padding: 10px;
	border: 1px solid black;
	cursor: pointer;
	margin-bottom: 30px;
}
.selected {
	background-color: grey;
}
</style>
