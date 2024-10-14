<template>
    <DialogShadowScreen>
        <div class="dialog out">
            <p class="content"> Вы уверены, что хотите выйти? <br/><br/> 
                Все ваши ответы будут сохранены, вы<br/>сможете вернуться к решению задач<br/>позже 
            </p>
            <div class="button_area">
                <button type="button" @click="hideDialog"> Отмена </button>
                <button type="button" @click="logout"> Выйти </button>
            </div>
        </div>
    </DialogShadowScreen>
</template>

<script>

export default {
    methods: {
        hideDialog() {
            this.$emit('hideDialog')
        },
        logout() {
            this.$auth.logout()
        },
    }
}
</script>

<style scoped>
.dialog {
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	-webkit-transform: translate(-50%, -50%);
	padding: 40px 60px;
	gap: 40px;
	border-radius: 20px;
	background: #1E8B93;
	flex-direction: column;
	justify-content: flex-start;
	z-index: 4;
    display: inline-flex;
    animation: show 0.2s;
}

.content {
	color: white;
	font-size: 24px;
	font-family: Montserrat Alternates;
	font-weight: 500;
}

.button_area {
    display: inline-flex;
	justify-content: space-between;
	gap: 40px;
	align-self: stretch;
}

button{
    user-select: none;
	-webkit-user-select: none;
	cursor: pointer;
	width: 270px;
	padding: 10px 0;
	background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%); 
	box-shadow: 7px 7px 6.699999809265137px #1A5866; 
    border-style: none;
	border-radius: 10px;
	font-size: 24px;
	font-weight: 600;
	text-align: center;
	font-size: 24px;
	font-family: Montserrat;
	font-weight: 600;
}

@media (max-width: 800px) {
	.dialog {
		padding: 16px;
		gap: 16px;
		border-radius: 16px;
	}

	.content {
		font-size: 14px;
	}

	.button_area {
		gap: 16px;
	}

	button {
		width: auto;
		font-size: 14px;
		border-radius: 8px;
		padding: 6px 8px;
		width: 147px;
	}
}
</style>