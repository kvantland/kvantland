<template>
    <div class="content_wrapper">
        <div class="advert_form">
            <div class="header"> {{ title }} </div>
            <template v-if="canSend">
                <p class="description">
                    Письмо для подтверждения адреса
                    электронной почты,</br> 
                    привязанной	к Вашему аккаунту, успешно отправлено!</br>
                    Для подтверждения адреса, перейдите по ссылке в</br>
                    письме, которое придёт Вам на почту
                </p>
                <FormField :fieldInfo="formFieldInfo" :value="email" :readonly="readonly" />
                <p v-if="remainedTimeToSend > 0" class="timer"> Отправить еще раз через: {{ remainedTimeToSend }}</p>
                <SubmitButton v-else-if="remainedTimeToSend == 0" @click="sendAgain"> Отправить еще раз </SubmitButton>
            </template>
            <div v-else class="limit_info">
                <img src="/icons/info.svg" />
                <p class="err"> Превышен лимит писем за день! </p>
            </div>
        </div>
    </div>
</template>

<script>
import SubmitButton from './Form/SubmitButton.vue';

export default {
    props: ['title', 'email'],

    data() {
        return {
            canSend: true,
            formFieldInfo: {
                'type': "input",
                'inputType': "email",
                'name': "email",
                'placeholder': "Почта",
            },
            readonly: true,
            remainedTimeToSend: 60,
        }
    },

    async fetch() {
        const newEmail = this.email
        let status = true
        this.$axios.$post('/api/check_email_amount', {'email': newEmail})
            .then((res) => {status = res.status})
        this.canSend = status
    },

    watch: {
        async remainedTimeToSend(newValue) {
            if (newValue > 0)
                setTimeout(function(){this.remainedTimeToSend -= 1}.bind(this), 1000)
        }
    },

    async mounted() {
        console.log(this.remainedTimeToSend)
        setTimeout(function(){this.remainedTimeToSend -= 1}.bind(this), 1000)
    },

    methods: {
        sendAgain() {

        },
    }
}
</script>

<style>
.content_wrapper {
	width: 100%;
	margin-top: 152px;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	display: inline-flex;
	margin-bottom: 40px;
}

.field {
    width: auto;
}

.advert_form {
	-webkit-user-select: none;
	user-select: none;
	display: inline-flex;
	flex-direction: column;
	justify-content: space-between;
	padding: 40px;
	gap: 21px;
	background: white;
	box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.10); 
	border-radius: 20px;
	margin: 0 auto;
}

.advert_form .header {
	text-align: center;
	color: black;
	font-size: 16px;
	font-weight: 700;
	text-transform: uppercase;
}

.advert_form .description {
	color: black;
	align-self: stretch;
	font-size: 14px;
	font-weight: 500;
}

.advert_form .limit_info {
	align-self: stretch;
	display: inline-flex;
	align-items: center;
	gap: 16px;
}

.advert_form .limit_info .err {
	color: #B62C5A;
	font-size: 12px;
	font-weight: 500;
}

.timer {
	font-size: 14px;
	text-align: center;
	align-self: stretch;
}
</style>