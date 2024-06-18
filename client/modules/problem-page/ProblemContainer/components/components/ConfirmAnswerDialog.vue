<template>
    <DialogShadowScreen>
        <div class="confirm_notification dialog">
            <p class="confirm_text">Готовы отправить ответ? <br/>Изменить его позже будет нельзя!</p>
            <div class="button_area">
                <button @click="sendAnswer"> Да </button>
                <button @click="hideConfirmDialog"> Нет </button>
            </div>
        </div>
    </DialogShadowScreen>
</template>

<script>
export default {
    methods: {
        sendAnswer() {
            this.$emit('sendAnswer')
        },
        hideConfirmDialog() {
            this.$emit('hideConfirmDialog')
        }
    }
}
</script>

<style scoped>
.shadow{
    position: fixed;
    z-index: 3;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.25);
}

.confirm_notification {
    font-family: Montserrat Alternates;
    font-size: 24px;
    font-weight: 600;
    color: white;
    display: inline-flex;
    flex-direction: column;
	justify-content: center;
	align-items: stretch;
	padding: 60px 40px;
	background: #1E8B93;
	border-radius: 20px;
	gap: 40px;
	z-index: 4;
	position: fixed;
	top:50%;
	left:50%;
	transform: translate(-50%, -50%);
	-webkit-transform: translate(-50%, -50%);
}

.button_area {
    display: inline-flex;
    align-items: stretch;
    gap: 40px;
}

button {
    cursor: pointer;
    font-family: Montserrat;
    font-size: 24px;
    font-weight: 600;
    flex: 1 1 0;
    padding: 10px 0;
    border-style: none;
    border-radius: 10px;
    box-shadow: 7px 7px 6.7px 0px rgb(26, 88, 102);
    background: linear-gradient(180.00deg, rgb(178, 178, 178) -46.115%,rgb(255, 255, 255) 20.86%,rgb(255, 255, 255) 63.61%,rgb(178, 178, 178) 136.285%);
}
</style>