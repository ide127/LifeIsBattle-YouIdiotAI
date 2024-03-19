<template>
	<div class="container">
		<matrix-background />
		<h1 class="index-title">{{ content.title }}</h1>
		<div class="select-language">
			<div
				:class="{ selected: selectedLanguage === 'en' }"
				@click="selectLanguage('en')"
			>
				english
			</div>
			<div
				:class="{ selected: selectedLanguage === 'ko' }"
				@click="selectLanguage('ko')"
			>
				korean
			</div>
		</div>
		<div v-html="realtimeDescription" class="description"></div>
		<button @click="scrollIntoMessageSubmit">
			{{ content.challenge }}
		</button>
		<!-- <div class="gradation-wrap">
			<img
				class="background-image"
				src="@/assets/imgs/neonCity.png"
				alt=""
			/>
		</div> -->

		<div class="background-container">
			<div class="blurred-background">
				<img
					class="background-image2"
					src="@/assets/imgs/starBucks.png"
					alt="Cafe Background"
				/>
			</div>
			<div class="chat-container">
				<div class="ai-img">
					<img src="@/assets/imgs/ai.png" alt="" />
				</div>
				<div class="chat-wrap">
					<div class="chat-history" ref="chatHistory">
						<!-- message는 한 줄을 차지하지만, message-wrap은 글씨의 크기에 딱 맞게 설정하기 위함임 -->
						<div
							class="message"
							v-for="(msg, index) in messages"
							:key="index"
							:class="{
								'align-right': msg.type === 'You',
								'align-left': msg.type === 'AI',
							}"
						>
							<div
								class="message-wrap"
								:class="{
									'align-right': msg.type === 'You',
									'align-left': msg.type === 'AI',
								}"
							>
								<p class="text">{{ msg.text }}</p>
								<p class="timestamp">
									<strong>{{ msg.type }}</strong>
									{{
										new Date(msg.timestamp).toLocaleString()
									}}
								</p>
							</div>
						</div>
					</div>
					<form
						@submit.prevent="sendMessage"
						v-if="
							winOrLoseBoolean != true &&
							winOrLoseBoolean != false
						"
					>
						<input
							type="text"
							v-model="newMessage"
							:placeholder="content.message_place_holder"
						/>
						<button type="submit">
							{{ content.message_button }}
						</button>
					</form>
				</div>
				<div class="human-img">
					<img src="@/assets/imgs/human.png" alt="" />
				</div>
			</div>
		</div>
		<div class="winOrLoseContainer">
			<a
				v-if="winOrLoseBoolean === true"
				@click.prevent="openWinModal"
				class="win-message"
				>{{ content.win_message }}</a
			>
			<a
				v-else-if="winOrLoseBoolean === false"
				@click.prevent="openLoseModal"
				>{{ content.fail_message }}</a
			>
		</div>

		<div class="ranking-board">
			<h1>{{ content.leaderboard.title }}</h1>
			<div
				class="leaderboard-description"
				v-html="content.leaderboard.description"
			></div>
			<div class="language-filters">
				<label>
					<input
						type="checkbox"
						v-model="filterLanguages.en"
						checked
					/>
					English
				</label>
				<label>
					<input
						type="checkbox"
						v-model="filterLanguages.ko"
						checked
					/>
					Korean
				</label>
			</div>
			<caption></caption>
			<thead>
				<tr>
					<th class="rank">Rank</th>
					<th class="nickname">Nickname</th>
					<th class="language">Language</th>
					<th class="score">Score</th>
				</tr>
			</thead>
			<div class="table-container" @scroll="handleScroll">
				<table>
					<tbody>
						<tr v-for="(user, index) in visibleUsers">
							<td>{{ index + 1 }}</td>
							<td>{{ user.nickname }}</td>
							<td>{{ user.language }}</td>
							<td>{{ Number(user.score).toFixed(2) }}</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
		<div class="cheating-strategy">
			<h2>{{ content.example_hint.title }}</h2>
			<div
				v-html="content.example_hint.description"
				class="cheating-strategy-description"
			></div>
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
	</div>
	<footer>
		<p>Copyright &copy; 2024 김준영 All Rights Reserved.</p>
	</footer>
	<!--
	<button @click="openWinModal">이겼습니다.</button>
	<button @click="openLoseModal">졌습니다.</button> -->

	<WinModal
		:isVisible="showModal"
		:score="score"
		:session="currentSession"
		:characterNumber="characterNumber"
		:selectedLanguage="selectedLanguage"
		:winOrLose="winOrLose"
		@onScrollIntoLeaderBoard="onScrollIntoLeaderBoard"
		@reloadRecords="loadRecords"
		@update:isVisible="showModal = $event"
	/>
</template>

<script setup lang="ts">
import languageData from "~/assets/language_resource.json";
import { useRequestHeaders } from "#app";
import { get } from "lodash-es";

const { $api } = useNuxtApp();

const showModal = ref(false);

const messages = ref<Message[]>([]);
const newMessage = ref("");
const chatHistory = ref<HTMLElement | null>(null);

const time = ref();

const dateInstance = new Date();

const currentSession = ref<Session | null>(null);

interface Session {
	id: string;
	ip: string;
	OpenAI_thread_id: string;
	start_time: string;
	end_time: string;
	is_successful: boolean | null;
	user_ip: string;
	user_language: string;
}

interface Message {
	id: string | null;
	type: string;
	is_user: boolean;
	text: string;
	timestamp: string;
	session: string;
}

/**
 * 언어 선택
 */
const selectedLanguage = ref("en");
const content = computed(() => {
	return languageData[selectedLanguage.value as keyof typeof languageData];
});

function selectLanguage(language: string) {
	selectedLanguage.value = language;
}

const visibleCharPersent = ref(0);
let interval = null;
onMounted(() => {
	const interval = setInterval(() => {
		if (visibleCharPersent.value < 3000) {
			visibleCharPersent.value += 1;
		} else {
			clearInterval(interval);
		}
	}, 15);
});

onUnmounted(() => {
	if (interval) {
		clearInterval(interval);
	}
});

const realtimeDescription = computed(() => {
	let visibleChar = content.value.description.slice(
		0,
		Math.floor(
			(visibleCharPersent.value / 3000) * content.value.description.length
		)
	);
	return visibleChar;
});

function formatDate(timestamp: string, language: string) {
	const date = new Date(timestamp);
	return date.toLocaleString(language);
}

/**
 * chatting 하는 곳으로 이동하는 버튼
 */
function scrollIntoMessageSubmit() {
	const element = document.querySelector(".chat-container");
	if (element) {
		// scrollIntoView를 사용하여 요소로 스크롤
		element.scrollIntoView({ behavior: "smooth", block: "center" });
	}
}

/**
 * get ip
 */
const headers = useRequestHeaders();
const ip = computed(() => {
	const forwardedFor = headers["x-forwarded-for"];
	if (forwardedFor) {
		if (Array.isArray(forwardedFor)) {
			return forwardedFor[0];
		} else {
			const ips = forwardedFor.split(",").map((ip) => ip.trim());
			return ips[0];
		}
	}
	return headers["x-real-ip"] || headers["remote-addr"] || "unknown";
});

/**
 * 채팅 관련 로직
 */
// The return value format is Session

async function sendMessage() {
	/** 공백상태 체크 */
	if (newMessage.value.trim()) {
		// TODO: 스켈레톤 UI 구현 to show it is waiting for the response

		// if no session, create a new session
		if (!currentSession.value) {
			currentSession.value = await $api.chattingService.createSession({
				id: null,
				OpenAI_thread_id: null,
				start_time: dateInstance.toISOString(),
				end_time: null,
				is_successful: null,
				score: null,
				user_ip: ip.value,
				user_language: selectedLanguage.value,
			});
			if (!currentSession.value) {
				// Handle the error here. For example, you can throw an error or return from the function.
				throw new Error("Failed to create a new session");
			}
		}
		const inputMessage: Message = {
			id: null,
			type: "You",
			is_user: true,
			text: newMessage.value,
			timestamp: dateInstance.toISOString(),
			session: currentSession.value.id,
		};
		newMessage.value = "";
		messages.value.push(inputMessage);
		const answer_message = await $api.chattingService.createMessage(
			inputMessage
		);
		messages.value.push(answer_message);

		// 새로운 메세지 입력 후, 이에 맞춰 스크롤을 하단으로 내려줌.
		nextTick(() => {
			if (chatHistory.value) {
				chatHistory.value.scrollTop = chatHistory.value.scrollHeight;
			}
		});

		// check the target sentence is in the new answer message
		// if messages length is over 20, it's fail.
		if (answer_message.text.includes(content.value.victory_sentence)) {
			proceedResult(true);
		} else if (messages.value.length >= 20) {
			proceedResult(false);
		}
	}
}

const winOrLoseBoolean = ref<null | boolean>(null);

const characterNumber = ref(0);
const score = ref(0);

async function calcScore(): Promise<void> {
	characterNumber.value = messages.value.reduce((acc, cur) => {
		return acc + cur.text.length;
	}, 0);
	const response = await $api.chattingService.getScore({
		num_str: characterNumber.value,
		language: selectedLanguage.value,
	});
	score.value = response.score;
}

async function proceedResult(result: boolean) {
	// check the current session is null or not
	if (!currentSession.value) {
		throw new Error("Session is not created yet");
	}
	if (result) {
		winOrLoseBoolean.value = true;
		currentSession.value.is_successful = true;
		await calcScore();
	} else {
		winOrLoseBoolean.value = false;
		currentSession.value.is_successful = false;
	}
	currentSession.value.end_time = dateInstance.toISOString();
	await $api.chattingService.patchSession(currentSession.value);
}

const winOrLose = ref("win");

function onScrollIntoLeaderBoard() {
	const element = document.querySelector(".ranking-board");
	if (element) {
		// scrollIntoView를 사용하여 요소로 스크롤
		element.scrollIntoView({ behavior: "smooth", block: "center" });
	}
}
/**
 * ranking-board
 */
const { data: records, refresh: loadRecords } = await useAsyncData(async () => {
	const response = await $api.chattingService.getLeaderboardList({
		limit: 10,
		offset: 0,
	});
	return response.results;
});
interface Record {
	id: string;
	nickname: string;
	score: number;
	num_str: number;
	language: string;
	time: string;
	session: string;
}
const filterLanguages = ref({en : true, ko : true});

const visibleUsers = computed(() => {
	return records.value
		.filter((record) => filterLanguages.value[record.language])
		.sort((a, b) => b.score - a.score);
});

const handleScroll = async (event: Event) => {
	const tableContainer = event.target;
	if (tableContainer instanceof HTMLElement) {
		const scrollHeight =
			tableContainer.scrollHeight - tableContainer.clientHeight;
		const scrollTop = tableContainer.scrollTop;

		if (scrollTop == 0) {
			let elementsByClassNameElement = document.getElementsByClassName(
				"table-container"
			)[0] as HTMLElement;
			elementsByClassNameElement.style.overflow = "fix";
			setTimeout(() => {
				elementsByClassNameElement.style.overflow = "auto";
			}, 200);
		}

		if (scrollHeight - scrollTop < 200) {
			const recordsLength = records.value.length;
			const params = {
				limit: 5,
				offset: recordsLength,
			};
			const newRecords = await $api.chattingService.getLeaderboardList(
				params
			);
			records.value.push(...newRecords.results);
		}
	} else {
		throw new Error("tableContainer is not HTMLElement");
	}
};

function openWinModal() {
	winOrLose.value = "win";
	showModal.value = !showModal.value;
}
function openLoseModal() {
	winOrLose.value = "lose";
	showModal.value = !showModal.value;
}
</script>

<style>
@media (min-width: 768px) {
	footer p {
		font-family: sans-serif;
		padding: 40px 0;
		text-align: center;
	}

	body {
		color: white;
		/* background: black; */
		font-family: text-regular;
		font-size: large;
		margin-left: auto;
		margin-right: auto;
		max-width: 800px;
	}
	.container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center; /* 센터 정렬을 위해 추가합니다 */
		padding: 0 50px;
		h1.index-title {
			font-family: LifeisBattle;
			font-size: 3rem;
		}
		h2 {
			font-size: 2.5rem;
		}
	}

	.description {
		margin-bottom: 30px;
		text-align: center;
		font-size: 1.2rem;
	}

	.matrix-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
	}
	.select-language div {
		display: inline-block;
		padding: 10px;
		border: 1px solid black;
		cursor: pointer; /* 마우스 오버 시 포인터 변경 */
		margin-bottom: 30px;
	}
	.selected {
		background-color: grey;
	}
	.description {
		margin-bottom: 30px;
		text-align: center;
	}

	/**
  neocity img
   */
	.gradation-wrap {
		margin: 50px 0;
		position: relative;
		display: inline-block; /* 혹은 필요에 맞는 다른 display 속성 */
		width: 100%;
		.background-image {
			width: 100%;
			height: 400px;
		}
	}
	.gradation-wrap::before,
	.gradation-wrap::after {
		content: "";
		position: absolute;
		left: 0;
		right: 0;
		z-index: 1;
	}

	/* 이미지 상단의 그라데이션 */
	.gradation-wrap::before {
		top: 0;
		height: 15%; /* 그라데이션의 높이, 필요에 따라 조절 */
		background: linear-gradient(to bottom, black, transparent);
	}

	/* 이미지 하단의 그라데이션 */
	.gradation-wrap::after {
		bottom: 0;
		height: 20%; /* 그라데이션의 높이, 필요에 따라 조절 */
		background: linear-gradient(to top, black, transparent);
	}

	/**
  chatting
   */
	.background-container {
		position: relative;
		width: 100%;
		height: 600px;
		margin-top: 100px;
	}
	.winOrLoseContainer {
		margin-bottom: 100px;
	}
	.background-container::before,
	.background-container::after {
		content: "";
		position: absolute;
		left: 0;
		right: 0;
		z-index: 1;
	}

	/* 이미지 상단의 그라데이션 */
	.background-container::before {
		top: 0;
		height: 15%; /* 그라데이션의 높이, 필요에 따라 조절 */
		background: linear-gradient(to bottom, black, transparent);
	}

	/* 이미지 하단의 그라데이션 */
	.background-container::after {
		bottom: 0;
		height: 10%; /* 그라데이션의 높이, 필요에 따라 조절 */
		background: linear-gradient(to top, black, transparent);
	}

	.background-image,
	.background-image2 {
		position: relative;
		z-index: 0; /* 이미지가 그라데이션 뒤에 위치하도록 함 */
	}

	.blurred-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
	.background-image2 {
		width: 100%;
		height: auto;
		filter: blur(5px); /* 블러 효과 적용 */
	}
	.chat-container {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		z-index: 1;
		display: flex;
		flex-direction: row;
		width: 100%;
		justify-content: space-between;
		margin-bottom: 30px;
		.ai-img {
			position: relative;
			width: 15%;
			display: flex;
			align-items: center;
			transform: rotateY(180deg);
			img {
				height: 320px;
			}
		}
		.human-img {
			width: 15%;
			display: flex;
			align-items: center;
			img {
				height: 320px;
			}
		}
		form {
			display: flex;
		}
		.chat-wrap {
			width: 60%;
		}
	}

	.chat-history {
		margin-bottom: 10px;
		padding: 15px;
		overflow-y: auto;
		height: 400px; /* Adjust based on your needs */
	}

	.message {
		.message-wrap {
			display: inline-block;
			max-width: 60%; /* 말풍선의 최대 너비 */
			margin-bottom: 10px;
			padding: 15px;
			border-radius: 20px; /* 말풍선 모양을 만듭니다 */
			background-color: #e1e1e1;
			color: black; /* 텍스트 색상 */
			.text {
				margin: 0;
				word-wrap: break-word; /* 긴 텍스트가 있을 경우 줄바꿈 */
			}
			.win-message {
				color: blue;
			}
		}
	}

	.align-right {
		align-items: flex-end !important; /* 오른쪽 정렬 */
		text-align: right;
		border-bottom-right-radius: 0 !important; /* 말풍선 꼬리 모양 조정 */
	}

	.align-left {
		align-items: flex-start !important; /* 왼쪽 정렬 */
		text-align: left;
		border-bottom-left-radius: 0 !important; /* 말풍선 꼬리 모양 조정 */
	}
	.timestamp {
		font-size: 0.8em;
		color: #666;
		margin-bottom: 0;
	}

	input[type="text"] {
		width: calc(100% - 75px);
		padding: 10px;
		margin-right: 10px;
		border: 1px solid #ccc;
		border-radius: 4px;
	}

	button {
		padding: 10px;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		display: flex;
	}

	/**
  ranking-board
   */
	.ranking-board {
		width: 700px;
		border: 1px solid #ccc;
		padding: 20px;
		margin-bottom: 100px;
		.leaderboard-description {
			font-size: large;
			margin-bottom: 20px;
			margin-top: 20px;
		}
		.table-container {
			max-height: 300px;
			width: 100%;
			overflow: auto;
		}

		table {
			width: 100% !important;
			border-collapse: collapse;
			table-layout: fixed; /* This will allow fixed table layouts */
		}
		caption,
		thead {
			width: 700px;
		}

		th,
		td {
			padding: 10px;
			border-bottom: 1px solid #ccc; /* This will create lines between rows */
			text-align: left; /* Aligns text to the left */
			white-space: nowrap; /* Prevents text from wrapping */
		}

		/* Setting width for th and td of Rank and Nickname */
		th:nth-child(1),
		td:nth-child(1),
		.rank {
			/* Rank */
			width: 10%; /* Minimum width */
			text-align: left;
		}
		th:nth-child(2),
		td:nth-child(2),
		.nickname {
			/* nickName */
			width: 20%;
			text-align: left;
		}

		/* Ensuring the Score column takes the rest of the space */
		th:nth-child(3),
		td:nth-child(3),
		.language {
			/* selectedLanguage */
			width: 50%;
			text-align: left;
		}
		th:nth-child(4),
		td:nth-child(4),
		.score {
			/* Score */
			width: 10%;
			text-align: center;
		}
	}

	/** cheating strategy */
	.cheating-strategy {
		margin-bottom: 30px;
		text-align: center;
		h2 {
			margin-bottom: 20px;
		}
	}
	.cheating-strategy-list-box {
		margin-top: 30px;
		display: grid;
		grid-template-columns: repeat(
			3,
			1fr
		); /* 3개의 열을 동일한 크기로 생성 */
		gap: 20px; /* 열과 행 사이의 간격 */
	}

	.strategy {
		display: flex;
		flex-direction: column;
		padding: 10px;
		border: 1px solid #ccc;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		border-radius: 5px;
		background-color: black;
		overflow: hidden;
	}
}

/* 모바일 화면 */
@media (max-width: 767px) {
	html,
	body,
	#__nuxt {
		display: flex;
		width: 414px;
		overflow-x: hidden;
	}
	body {
		color: white;
		background: black;
		font-family: text-regular;
		font-size: large;
	}
	.container {
		display: flex;
		width: 414px;
		flex-direction: column;
		justify-content: center;
		align-items: center; /* 센터 정렬을 위해 추가합니다 */
		.index-title {
			width: 250px;
			text-align: center;
			font-family: LifeisBattle;
		}
	}

	.select-language div {
		display: inline-block;
		padding: 10px;
		border: 1px solid black;
		cursor: pointer; /* 마우스 오버 시 포인터 변경 */
		margin-bottom: 30px;
	}
	.selected {
		background-color: grey;
	}
	.description {
		width: 354px;
		margin-bottom: 30px;
		text-align: center;
	}

	img,
	.ai-img,
	.human-img {
		display: none !important;
	}

	.background-container {
		position: relative;
		width: 100%;
		height: 600px;
		margin-top: 100px;
	}
	.chat-container {
		width: 100%;
		min-height: 300px;
		background-color: white;
		form {
			display: flex;
		}
		.chat-wrap {
			margin: 50px 0;
		}
		.chat-history {
			margin-bottom: 10px;
			padding: 15px;
			overflow-y: auto;
			height: 400px; /* Adjust based on your needs */
		}
		.message {
			.message-wrap {
				display: inline-block;
				max-width: 60%; /* 말풍선의 최대 너비 */
				margin-bottom: 10px;
				padding: 15px;
				border-radius: 20px; /* 말풍선 모양을 만듭니다 */
				background-color: #e1e1e1;
				color: black; /* 텍스트 색상 */
				.text {
					margin: 0;
					word-wrap: break-word; /* 긴 텍스트가 있을 경우 줄바꿈 */
				}
				.win-message {
					color: blue;
				}
			}
		}

		.align-right {
			margin-right: 10px;
			align-items: flex-end !important; /* 오른쪽 정렬 */
			text-align: right;
			border-bottom-right-radius: 0 !important; /* 말풍선 꼬리 모양 조정 */
		}

		.align-left {
			align-items: flex-start !important; /* 왼쪽 정렬 */
			text-align: left;
			border-bottom-left-radius: 0 !important; /* 말풍선 꼬리 모양 조정 */
		}
		.timestamp {
			font-size: 0.8em;
			color: #666;
			margin-bottom: 0;
		}

		input[type="text"] {
			width: calc(100% - 135px);
			margin: 10px;
			padding: 10px;
			margin-right: 10px;
			border: 1px solid #ccc;
			border-radius: 4px;
		}

		button {
			margin: 10px;
			padding: 10px;
			border: none;
			border-radius: 4px;
			cursor: pointer;
			display: flex;
		}
	}

	.ranking-board {
		width: 70%;
		border: 1px solid #cccccc;
		padding: 20px;
		margin-bottom: 30px;
		h1 {
			width: 220px;
		}
		.leaderboard-description {
			font-size: small;
			padding-bottom: 20px;
		}
		.table-container {
			width: 100%;
			max-height: 300px;
			overflow: auto;
		}

		table {
			width: 97% !important;
			border-collapse: collapse;
			table-layout: fixed; /* This will allow fixed table layouts */
		}

		th,
		td {
			padding: 10px;
			border-bottom: 1px solid #ccc; /* This will create lines between rows */
			text-align: left; /* Aligns text to the left */
			white-space: nowrap; /* Prevents text from wrapping */
		}

		/* Setting width for th and td of Rank and Nickname */
		th:nth-child(1),
		td:nth-child(1) {
			/* Rank */
			width: 10%; /* Minimum width */
			text-align: center;
		}
		th:nth-child(2),
		td:nth-child(2) {
			/* nickName */
			width: 30%;
			text-align: left;
		}

		/* Ensuring the Score column takes the rest of the space */
		th:nth-child(3),
		td:nth-child(3) {
			/* selectedLanguage */
			width: 10%;
			text-align: left;
		}
		th:nth-child(4),
		td:nth-child(4) {
			/* Score */
			width: 10%;
			text-align: right;
		}
	}

	/** cheating strategy */
	.cheating-strategy {
		margin-bottom: 30px;
		text-align: center;
	}
	.cheating-strategy-description {
		align-content: center;
		justify-content: center;
		align-items: center;
		justify-items: center;
		p {
			width: 100%;
			padding: 5%;
		}
		width: 364px;
	}
	.cheating-strategy-list-box {
		display: grid;
		grid-template-columns: repeat(
			1,
			1fr
		); /* 3개의 열을 동일한 크기로 생성 */
		gap: 20px; /* 열과 행 사이의 간격 */
	}

	.strategy {
		display: flex;
		width: 90%;
		flex-direction: column;
		padding: 10px;
    margin-left : 10px;
		border: 1px solid #ccc;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		border-radius: 5px;
		background-color: black;
		overflow: hidden;
	}
  footer {
    text-align: center;
  }
}
</style>
