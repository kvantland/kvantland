<template>
    <div class="input_area">
        <p class="input_label"> Введите ответ: </p>
        <input class="answer_input" name="answer" type="number" v-model="answer" required/>
        <AnswerButton @sendAnswer="sendAnswer"/>
    </div>
</template>

<script>
import AnswerButton from './AnswerButton.vue'
import ConfirmDialog from './ConfirmDialog.vue'

export default {
    components: {
        AnswerButton,
        ConfirmDialog,
    },

    data(){
        return {
            showConfirmDialogMode: false,
            answer: "",
        }
    },

    methods: {
        sendAnswer() {
            this.showConfirmDialogMode = false
            this.$emit('sendAnswer', this.answer)
        }
    }
}
</script>

<style scoped>
.input_area {
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