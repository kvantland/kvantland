<template>
    <div class="content_wrapper">
        <div class="advert_form">
            <div class="header"> {{ title }} </div>
            <p class="description" v-html="description" />
            <FormField :fieldInfo="formFieldInfo" :value="email" :readonly="readonly" :error="error" @input="changeEmail" @clearError="clearError" />
            <p v-if="remainedTimeToSend > 0" class="timer"> Отправить еще раз через: {{ remainedTimeToSend }}</p>
            <button v-else-if="remainedTimeToSend == 0" class="send_again" @click="sendAgain($event.target.value)"> Отправить еще раз </button>
            <slot />
        </div>
    </div>
</template>

<script>
import { readonly } from 'vue';

export default {
    props: {
        title:{}, 
        email:{default:""},
        description:{},
        formData:{}, 
        apiRequestUrl:{},
        readonly:{default:true},
        remainedTimeToSendProp:{default: 60},
    },

    data() {
        return {
            formFieldInfo: {
                'type': "input",
                'inputType': "email",
                'name': "email",
                'placeholder': "Почта",
            },
            timeToSendAgain: 60,
            error: "",
            remainedTimeToSend: this.remainedTimeToSendProp,

        }
    },

    watch: {
        async remainedTimeToSend(newValue) {
            if (newValue > 0)
                setTimeout(function(){this.remainedTimeToSend -= 1}.bind(this), 1000)
            else
                this.error = ""
        }
    },

    async mounted() {
        console.log(this.remainedTimeToSend)
        if (this.remainedTimeToSend > 0)
            setTimeout(function(){this.remainedTimeToSend -= 1}.bind(this), 1000)
    },

    methods: {
        async sendAgain() { 
            let status = ""
            await this.$axios.$post(this.apiRequestUrl, this.formData)
            .then((resp) => {
                console.log(resp)
                if (!resp.status){
                    console.log(resp.errors.email)
                    if (resp.errors.email == "Превышен лимит писем за день!")
                        status = "Превышен лимит писем за день!"
                    else
                        status = "Проверка не пройдена"
                    }
                })
            this.error = status
            console.log(this.error)
            this.remainedTimeToSend = this.timeToSendAgain
        },
        changeEmail(newValue) {
            this.$emit('changeEmail', newValue)
        },
        clearError() {
            this.error=""
        }
    },
}
</script>

<style scoped>
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

.send_again {
    cursor: pointer;
    align-self: stretch;
    padding: 0 20px;
    height: 50px;
    font-size: 14px;
    font-weight: 600;
    background: #1E8B93;
    box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25);
    border-radius: 6px;
    color: white;
    border: none;
    font-family: Montserrat;
}
</style>