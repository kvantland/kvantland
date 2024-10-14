<template>
    <div>
        <SendToEmailForm
		v-if="pwRecoveryMode"
            :title="pwRecovery.title" :description="pwRecovery.description" :readonly="false" :email="pwRecovery.email"
            :form-data="{'email': pwRecovery.email}" :api-request-url="pwRecovery.api" :remained-time-to-send-prop="pwRecovery.timeToSendAgain"
            @changeEmail="changeEmail">
            <p class="backToAuthLink" @click="backToAuth"> Авторизоваться </p> 
        </SendToEmailForm>
        <Form v-else>
            <FormHeader mode="auth" @changeHeaderMode="changeHeaderMode" />
            <form :id="id" method="post" @submit.prevent="onSubmitAuthForm">
                <FieldsArea>
                    <FormField
					v-for="field in loginFields" :key="field.name" v-model="fields[field.name]"
                    :field-info="field" :error="errors[field.name]" @clearError="clearError"/>
                </FieldsArea>
                <SubmitButton :form="id"> Войти </SubmitButton>
            </form>
                <hr size="1" style="border-width: 1px" />
                <VkAuthButton />
                <p class="pwRecoveryLink" @click="startPwRecovery" >
                    Восстановить пароль
                </p>
        </Form>
    </div>
</template>

<script>
import FormHeader from './components/FormHeader'

export default {

    components: {
        FormHeader,
    },
    props: ['loginFields'],

    data() {
        return {
            id: 'login',
            fields: {},
            errors: {},
            pwRecoveryMode: false,
            pwRecovery: {
                email: "",
                api: "/api/pw_recovery",
                title: "Восстановление пароля",
                description:  `Введите адрес электронной почты,
                            <br/> привязанной к Вашему аккаунту `,
                timeToSendAgain: 0,
            },
        }
    },

    methods: {
        changeHeaderMode(modeToChange) {
            this.$emit('changeHeaderMode', modeToChange)
        },
        async onSubmitAuthForm() {
            console.log('auth!')
            await this.$auth.loginWith('local', {data:this.fields})
            .then((res) => {
                if (res.data.status) {
                    this.$auth.setUserToken(res.data.tokens.access_token, res.data.tokens.refresh_token)
                    this.$auth.setUser(res.data.user)
                }
                else {
                    this.errors = res.data.errors
                }
            })
        },
        changeEmail(newValue) {
            this.pwRecovery.email = newValue
        },
        backToAuth(){
            this.pwRecoveryMode = false
        },
        startPwRecovery() {
            this.pwRecoveryMode = true
        },
        clearError(name) {
            this.errors[name] = ''
        }
    }
}
</script>

<style scoped>
.pwRecoveryLink {
    display: inline-flex;
    text-decoration: underline;
    color: #1E8B93;
    font-size: 14px;
    font-weight: 500;
    align-self: stretch;
    text-align: right;
    flex-direction: row-reverse;
    cursor: pointer;
}

.backToAuthLink {
    display: inline-flex;
    text-decoration: underline;
    color: #1E8B93;
    font-size: 14px;
    font-weight: 500;
    align-self: stretch;
    text-align: right;
    flex-direction: row-reverse;
    cursor: pointer;
}
</style>