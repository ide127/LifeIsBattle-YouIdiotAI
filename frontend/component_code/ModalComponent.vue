<template>
	<button @click="openModal">이겼습니다.</button>
	<button @click="openModal2">졌습니다.</button>

	<WinModal
		:isVisible="showModal"
		:score="score"
		:selectedLanguage="selectedLanguage"
		:winOrLose="winOrLose"
		@onScrollIntoLeaderBoard="onScrollIntoLeaderBoard"
		@update:isVisible="showModal = $event"
	/>
</template>

<script setup lang="ts">
const showModal = ref(false);
const score = ref(0);
const winOrLose = ref("win");

function openModal() {
	winOrLose.value = "win";
	showModal.value = !showModal.value;
}
function openModal2() {
	winOrLose.value = "lose";
	showModal.value = !showModal.value;
}

function onScrollIntoLeaderBoard() {
	const element = document.querySelector(".ranking-board");
	if (element) {
		element.scrollIntoView({ behavior: "smooth", block: "center" });
	}
}
</script>
