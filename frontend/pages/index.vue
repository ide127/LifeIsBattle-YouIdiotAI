<template>
	<div class="container">
		<h1>{{ content.title }}</h1>
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

		<div v-html="content.description" class="description"></div>
		<button @click="scrollIntoMessageSubmit">
			{{ content.challenge }}
		</button>
		<div class="gradation-wrap">
			<img
				class="background-image"
				src="@/assets/imgs/neonCity.png"
				alt=""
			/>
		</div>

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
									{{ msg.timestamp }}
								</p>
							</div>
						</div>
					</div>
					<form @submit.prevent="sendMessage">
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
	</div>

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
import languageData from "~/assets/language_resource.json";
import { useRequestHeaders } from "#app";

const { $api } = useNuxtApp();

const showModal = ref(false);

const score = ref(0);

const messages = ref<Message[]>([]);
const newMessage = ref("");
const chatHistory = ref<HTMLElement | null>(null);

const time = ref();

const dateInstance = new Date();

let currentSession = ref<Session | null>(null);

interface Session {
	id: string;
	ip: string;
	OpenAI_thread_id: string;
	start_time: string;
	end_time: string;
	is_successful: any;
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
const selectedLanguage = ref("EN");
const content = computed(() => {
	return languageData[selectedLanguage.value as keyof typeof languageData];
});

function selectLanguage(language: string) {
	selectedLanguage.value = language;
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
				start_time: dateInstance.toLocaleTimeString(),
				end_time: null,
				is_successful: null,
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
			timestamp: dateInstance.toLocaleTimeString(),
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
			proceedResult(true, currentSession);
		} else if (messages.value.length >= 20) {
			proceedResult(false, currentSession);
		}
	}
}

function proceedResult(result: boolean, currentSession: ref<Session | null>) {
	if (result) {
		alert("You win!");
		currentSession.value.is_successful = true;
	} else {
		alert("You lose!");
		currentSession.value.is_successful = false;
	}
	currentSession.value.end_time = dateInstance.toLocaleTimeString();
	$api.chattingService.patchSession(currentSession.value);
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
// 더미 데이터로 시작
const users = ref([
	{ id: 1, nickname: "Player1", score: 500 },
	{ id: 2, nickname: "Player2", score: 400 },
	{ id: 3, nickname: "Player3", score: 300 },
	{ id: 4, nickname: "Player4", score: 200 },
	{ id: 5, nickname: "Player5", score: 100 },
	// 추가 사용자는 스크롤을 통해 볼 수 있습니다.
	{ id: 6, nickname: "Player6", score: 50 },
]);

function openModal() {
	winOrLose.value = "win";
	showModal.value = !showModal.value;
}
function openModal2() {
	winOrLose.value = "lose";
	showModal.value = !showModal.value;
}
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
	align-items: center; /* 센터 정렬을 위해 추가합니다 */
	padding: 0 50px;
	h1 {
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
	margin-bottom: 30px;
	text-align: center;
}

/**
background-image
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
	margin: 100px 0;
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
	filter: blur(10px); /* 블러 효과 적용 */
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
		width: 15%;
		display: flex;
		align-items: center;
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
	margin-bottom: 30px;
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
		text-align: left;
	}
	th:nth-child(2),
	td:nth-child(2) {
		/* nickName */
		width: 20%;
		text-align: left;
	}

	/* Ensuring the Score column takes the rest of the space */
	th:nth-child(3),
	td:nth-child(3) {
		/* selectedLanguage */
		width: 50%;
		text-align: left;
	}
	th:nth-child(4),
	td:nth-child(4) {
		/* Score */
		width: 10%;
		text-align: center;
	}
}

/** cheating strategy */
.cheating-strategy {
	margin-bottom: 30px;
	text-align: center;
}
.cheating-strategy-list-box {
	display: grid;
	grid-template-columns: repeat(3, 1fr); /* 3개의 열을 동일한 크기로 생성 */
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
</style>
