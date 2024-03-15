<template>
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
					<button type="submit">{{ content.message_button }}</button>
				</form>
			</div>
			<div class="human-img">
				<img src="@/assets/imgs/human.png" alt="" />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import languageData from "~/assets/language_resource.json";
import { useRequestHeaders } from "#app";

const { $api } = useNuxtApp();

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

const messages = ref<Message[]>([]);
const newMessage = ref("");
const chatHistory = ref<HTMLElement | null>(null);

const time = ref();
const dateInstance = new Date();
let currentSession = ref<Session | null>(null);

const selectedLanguage = inject("selectedLanguage");
const content = computed(() => languageData[selectedLanguage.value]);

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
</script>

<style>
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
.background-container::before {
	top: 0;
	height: 15%;
	background: linear-gradient(to bottom, black, transparent);
}
.background-container::after {
	bottom: 0;
	height: 10%;
	background: linear-gradient(to top, black, transparent);
}
.background-image,
.background-image2 {
	position: relative;
	z-index: 0;
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
	filter: blur(10px);
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
}
.ai-img {
	width: 15%;
	display: flex;
	align-items: center;
}
.ai-img img {
	height: 320px;
}
.human-img {
	width: 15%;
	display: flex;
	align-items: center;
}
.human-img img {
	height: 320px;
}
.chat-wrap {
	width: 60%;
}
.chat-history {
	margin-bottom: 10px;
	padding: 15px;
	overflow-y: auto;
	height: 400px;
}
.message .message-wrap {
	display: inline-block;
	max-width: 60%;
	margin-bottom: 10px;
	padding: 15px;
	border-radius: 20px;
	background-color: #e1e1e1;
	color: black;
}
.message .message-wrap .text {
	margin: 0;
	word-wrap: break-word;
}
.align-right {
	align-items: flex-end !important;
	text-align: right;
	border-bottom-right-radius: 0 !important;
}
.align-left {
	align-items: flex-start !important;
	text-align: left;
	border-bottom-left-radius: 0 !important;
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
</style>
