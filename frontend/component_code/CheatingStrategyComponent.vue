<template>
	<div class="cheating-strategy">
		<h2>{{ content.example_hint.title }}</h2>
		<div v-html="content.example_hint.description"></div>
		<div class="cheating-strategy-list-box">
			<div
				class="strategy"
				v-for="strategy in content.example_hint.examples"
				:key="strategy.id"
			>
				<h3 class="title">{{ strategy.title }}</h3>
				<div class="text">{{ strategy.description }}</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import languageData from "~/assets/language_resource.json";

const selectedLanguage = inject("selectedLanguage");
const content = computed(() => languageData[selectedLanguage.value]);
</script>

<style>
.cheating-strategy {
	margin-bottom: 30px;
	text-align: center;
}
.cheating-strategy-list-box {
	display: grid;
	grid-template-columns: repeat(3, 1fr); /* 3개의 열을 동일한 크기로 생성 */
	gap: 20px; /* 열과 행 사이의 간격 */
}
</style>
