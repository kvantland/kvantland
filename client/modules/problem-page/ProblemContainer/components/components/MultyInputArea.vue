<template>
	<div class="multy-input-area">
		<div
			v-for="_, inputNum in answers"
			:key="`input-area_num-${inputNum}`"
			class="input-area">
			<p class="input_label"> Введите ответ: </p>
			<input v-model="answers[inputNum]" class="answer_input" name="answer" type="number" required/>
			<img
				v-if="inputNum === answers.length - 1"
				class="input-button input-button_add" src="/problem_assets/add-button.svg"
				@click="addInput" />
			<img 
				class="input-button input-button_delete" src="/problem_assets/delete-button.svg"
				@click="deleteInput(inputNum)" />
		</div>
		<AnswerButton @sendAnswer="sendAnswer"/>
	</div>
</template>

<script>
import AnswerButton from './AnswerButton.vue';

export default {
	components: {
		AnswerButton,
	},
	data() {
		return {
			answers: [''],
		}
	},
	methods: {
		sendAnswer() {
			this.$emit('sendAnswer', this.answers)
		},
		deleteInput(inputNum) {
			this.answers.splice(inputNum, 1)
		},
		addInput() {
			this.answers.push('')
		},
	}
}
</script>

<style scoped>
.multy-input-area {
	display: inline-flex;
	flex-direction: column;
	gap: 20px;
}

.input-button {
	width: 30px;
	height: 30px;
	cursor: pointer;
}

.input-area {
    display: inline-flex;
    gap: 20px;
    align-items: center;
}
.answer_input {
  -moz-appearance: textfield;
	width: 160px;
	height: 30px;
	padding-left: 20px;
	padding-right: 20px;
	padding-top: 10px;
	padding-bottom: 10px;
	background: white;
	border-radius: 10px;
	font-size: 24px;
	font-family: Montserrat;
	font-weight: 500;
	word-wrap: break-word;
}

.input_label {
	color: white;
	font-size: 24px;
	font-family: Montserrat;
	font-weight: 500;
	word-wrap: break-word
}
</style>