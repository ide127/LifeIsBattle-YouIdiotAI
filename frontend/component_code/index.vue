<template>
	<div class="container">
		<HeaderComponent />
		<LanguageSelector />
		<DescriptionComponent />
		<ChallengeButton />
		<BackgroundImage />
		<ChatComponent />
		<RankingBoard />
		<CheatingStrategyComponent />
		<ModalComponent />
	</div>
</template>

<script setup lang="ts">
import HeaderComponent from "./HeaderComponent.vue";
import LanguageSelector from "./LanguageSelector.vue";
import DescriptionComponent from "./DescriptionComponent.vue";
import ChallengeButton from "./ChallengeButton.vue";
import BackgroundImage from "./BackgroundImage.vue";
import ChatComponent from "./ChatComponent.vue";
import RankingBoard from "./RankingBoard.vue";
import CheatingStrategyComponent from "./CheatingStrategyComponent.vue";
import ModalComponent from "./ModalComponent.vue";
</script>

<style>
body {
	color: white;
	background: black;
	font-family: text-regular;
	font-size: large;
}
.container {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	padding: 0 50px;
}
</style>
