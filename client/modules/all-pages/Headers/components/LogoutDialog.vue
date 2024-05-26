<template>
    <div>
        <div class="shadow"></div>
        <div class="dialog out">
            <p class="content"> Вы уверены, что хотите выйти? <br/><br/> 
                Все ваши ответы будут сохранены, вы<br/>сможете вернуться к решению задач<br/>позже 
            </p>
            <div class="button_area">
                <button type="button" @click="hideDialog"> Отмена </button>
                <button type="button" @click="logout"> Выйти </button>
            </div>
        </div>
    </div>
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
</style>