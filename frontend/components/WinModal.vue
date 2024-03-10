<template>
  <div v-if="isVisible" class="modal">
    <div class="modal-content" @click.stop>
      <p>{{ content.win_comments.line1 }}</p>
      <p>{{ content.win_comments.line2 }}</p>
      <h2>{{ content.win_comments.line3 }}</h2>
      <p>{{ content.win_comments.line4_1 }} {{props.score}}{{ content.win_comments.line4_2 }}</p>
      <p>{{ content.win_comments.line5 }}</p>
      <p>{{ content.win_comments.line6 }}</p>
      <div>
        <form @submit.prevent="sendNickname">
          <input ref="inputRef" type="text" v-model="nickName"/>
          <button type="submit">{{ content.win_comments.button1 }}</button>
        </form>
      </div>
      <div class="exit-button-container">
        <button @click="close">{{ content.win_comments.button2 }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import languageData from '~/assets/language_resource.json'

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