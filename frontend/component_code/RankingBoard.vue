<template>
	<div class="ranking-board">
		<h1>{{ content.leaderboard.title }}</h1>
		<div
			class="leaderboard-description"
			v-html="content.leaderboard.description"
		></div>
		<div class="table-container">
			<table>
				<thead>
					<tr>
						<th>Rank</th>
						<th>Nickname</th>
						<!-- TODO: 언어별 sort하는 버튼 만들기 -->
						<th>language</th>
						<th>Score</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(user, index) in users" :key="user.id">
						<td>{{ index + 1 }}</td>
						<td>{{ user.nickname }}</td>
						<td>{{ selectedLanguage }}</td>
						<td>{{ user.score }}</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script setup lang="ts">
import languageData from "~/assets/language_resource.json";

const selectedLanguage = inject("selectedLanguage");
const content = computed(() => languageData[selectedLanguage.value]);

const users = ref([
	{ id: 1, nickname: "Player1", score: 500 },
	{ id: 2, nickname: "Player2", score: 400 },
	{ id: 3, nickname: "Player3", score: 300 },
	{ id: 4, nickname: "Player4", score: 200 },
	{ id: 5, nickname: "Player5", score: 100 },
	{ id: 6, nickname: "Player6", score: 50 },
]);
</script>

<style>
.ranking-board {
	width: 700px;
	border: 1px solid #ccc;
	padding: 20px;
	margin-bottom: 30px;
}
.leaderboard-description {
	font-size: small;
	padding-bottom: 20px;
}
.table-container {
	width: 100%;
	overflow-x: auto;
}
table {
	width: 100%;
	border-collapse: collapse;
	table-layout: fixed;
}
th,
td {
	padding: 10px;
	border-bottom: 1px solid #ccc;
	text-align: left;
	white-space: nowrap;
}
th:nth-child(1),
td:nth-child(1) {
	width: 10%;
	text-align: left;
}
th:nth-child(2),
td:nth-child(2) {
	width: 20%;
	text-align: left;
}
th:nth-child(3),
td:nth-child(3) {
	width: 50%;
	text-align: left;
}
th:nth-child(4),
td:nth-child(4) {
	width: 10%;
	text-align: center;
}
</style>
