<template>
  <div v-if="isVisible" class="modal">
    <div v-if="props.winOrLose=='win'" class="modal-content" @click.stop>
      <p>{{ content.success.title }}</p>
      <p>{{ content.success.sub_title }}</p>
      <h2>{{ content.success.your_score }}</h2>
      <p>{{ content.success.score1 }} {{props.score}}{{ content.success.score2 }}</p>
      <p>{{ content.success.score_desc }}</p>
      <p>{{ content.success.post_desc }}</p>
      <div>
        <form @submit.prevent="sendNickname">
          <input ref="inputRef" type="text" v-model="nickName"/>
          <button type="submit">{{ content.success.post_button }}</button>
        </form>
      </div>
      <div class="exit-button-container">
        <button @click="close">{{ content.success.exit_button }}</button>
      </div>
    </div>

    <div v-else class="modal-content" @click.stop>
      <p>{{ content.fail.title }}</p>
      <p>{{ content.fail.sub_title }}</p>
      <button @click="onScrollIntoLeaderBoard">{{ content.fail.see_leaderboard }}</button>
      <div class="exit-button-container">
        <button @click="close">{{ content.fail.exit_button }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import languageData from '~/assets/gameOver_modal_language_resource.json'

const content = computed(() => {
  return languageData[props.selectedLanguage];
});

const nickName = ref('');
const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  score: {
    type: Number,
    default: 0
  },
  selectedLanguage:{
    type: String,
    default: "EN"
  },
  winOrLose:{
    type:String,
    default:"Lose"
  }
});

// 모달 열고 닫을 때마다 nickName 값 초기화
watch(()=>props.isVisible, ()=>{
  nickName.value = '';
})

const inputRef = ref(null);
function sendNickname() {
  if (nickName.value === '') {
    // nickName이 빈 문자열이거나 공백만 있는 경우
    inputRef.value.focus();
  } else {
    // 닉네임이 제대로 입력된 경우, 여기에 원하는 로직을 구현
    console.log('등록된 닉네임:', nickName.value);
    close();
    // 예: 서버로 닉네임 전송
  }
}

const emit = defineEmits(['update:isVisible']);

function onScrollIntoLeaderBoard() {
  emit('onScrollIntoLeaderBoard');
  close();
}

const close = () => {
  emit('update:isVisible', false);
};
</script>

<style>
.modal {
  display: block; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-items: center;
  p{
    color: black !important;
  }
  h2{
    color: black !important;
  }
}

.modal-content form {
  display: flex; /* 입력 필드와 등록하기 버튼을 옆으로 정렬 */
  align-items: center; /* 세로 축 중앙 정렬 */
}

.modal-content form input {
  width: 200px;
  margin-right: 10px; /* 입력 필드와 버튼 사이의 간격 */
}

.exit-button-container {
  text-align: center; /* 나가기 버튼을 중앙 정렬 */
  margin-top: 20px; /* 나가기 버튼과 그 위의 내용 사이 간격 */
}
</style>