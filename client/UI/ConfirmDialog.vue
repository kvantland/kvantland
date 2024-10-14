<template>
    <DialogShadowScreen>
        <div class="confirm_dialog">
            <div class="header">
                <div class="title">
                    <img class="info" src="/icons/warning.svg" />
                    <p> Обрати внимание! </p>
                </div>
            </div>
            <p class="body"> {{ content }} </p>
            <div class="button_area">
                <div class="button accept_button" @click="confirmAction(true)"> {{ acceptText }} </div>
                <div class="button refuse_button" @click="confirmAction(false)"> {{ refuseText }} </div>
            </div>
        </div>
    </DialogShadowScreen>
</template>

<script>
export default {
    props: ['params'],

    computed: {
        content() {
            return this.params.content
        },
        acceptText() {
            return this.params.acceptText
        },
        refuseText() {
            return this.params.refuseText
        },
    },

    methods: {
        confirmAction(status) {
            this.$emit('confirmAction', status)
        }
    },
}
</script>

<style scoped>
.confirm_dialog {
    opacity: 1;
    animation: show 0.4s;
    min-width: 500px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: inline-flex;
    flex-direction: column;
    gap: 40px;
    padding: 40px 60px;
    background: rgb(30, 139, 147);
    border-radius: 20px;
    font-family: Montserrat;
    color: white;
    font-weight: 600;
    font-size: 24px;
}

@keyframes show {
    0% {opacity: 0;}
    100% {opacity: 1;}
}

.header {
    display: inline-flex;
    align-items: center;
    justify-content: space-between;

}

.title {
    display: inline-flex;
    gap: 17px;
    align-items: center;
}

.info {
    width: 30px;
    height: 30px;
}

.cross {
    cursor: pointer;
    width: 24px;
    height: 24px;
}

.button_area {
    display: inline-flex;
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
    gap: 30px;
}

.button {
    width: 100%;
    text-align: center;
    color: black;
    cursor: pointer;
    font-family: Montserrat;
    font-size: 24px;
    font-weight: 600;
    padding: 10px 0;
    border-style: none;
    border-radius: 10px;
    box-shadow: 7px 7px 6.7px 0px rgb(26, 88, 102);
    background: linear-gradient(180.00deg, rgb(178, 178, 178) -46.115%,rgb(255, 255, 255) 20.86%,rgb(255, 255, 255) 63.61%,rgb(178, 178, 178) 136.285%);
}

@media (max-width: 800px) {
	.confirm_dialog {
		padding: 16px;
		gap: 16px;
		border-radius: 16px;
		font-size: 12px;
		min-width: 0px;
		width: auto;
	}

	.button_area {
		gap: 16px;
	}

	.button {
		width: auto;
		font-size: 14px;
		border-radius: 8px;
		padding: 6px 8px;
		width: 120px;
	}

	.info {
		width: 18px;
		height: 18px;
	}
}

</style>
