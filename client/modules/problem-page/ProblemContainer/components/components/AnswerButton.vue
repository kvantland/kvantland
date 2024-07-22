<template>
    <div>
        <ConfirmAnswerDialog v-if="confirmMode" @sendAnswer="sendAnswer" @hideConfirmDialog="hideConfirmDialog" />
        <button class="answer_button" type="submit" form="problem_form" @click="showConfirmDialog"> Отправить </button>
    </div>
</template>

<script scoped>
import ConfirmAnswerDialog from  './ConfirmAnswerDialog.vue'

export default {
    data() {
        return {
            confirmMode: false
        }
    },

    components: {
        ConfirmAnswerDialog,
    },

    methods: {
        showConfirmDialog() {
            this.confirmMode = true
        },
        hideConfirmDialog() {
            this.confirmMode = false
        },
        sendAnswer() {
            this.$emit('sendAnswer')
        }
    }
}
</script>
<style scoped>
.answer_button {
    cursor: pointer;
    border: none;
    align-self: center;
    padding: 10px 0;
    border-radius: 10px;
    width: 200px;
    height: 50px;
    background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%);
    box-shadow: 7px 7px 7px #1A5866;
    text-align: center;
    color: black;
    font-size: max(20px, min(2.7vw, 24px));
    font-family: Montserrat;
    font-weight: 600;
    word-wrap: break-word;
}
</style>