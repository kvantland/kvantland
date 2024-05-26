<template>
    <Form>
        <p class="header"> Восстановление пароля </p>
        <form id="pw_recovery" @submit.prevent="submitPwRecovery">
            <FieldsArea>
                <FormField v-for="field in fieldsInfo" :fieldInfo="field" :key="field.name" 
                    v-model="fields[field.name]" :error="errors[field.name]"  @clearError="clearError" />
            </FieldsArea>
        </form>
        <SubmitButton :id="'pw_recovery'"> Отправить </SubmitButton>
    </Form>
</template>

<script>
export default {
    layout: 'forms',

    data() {
        return {
            fieldsInfo: [
                {'type': "input", 'inputType': "password", 'name':"password", 'placeholder':"Пароль"},
                {'type': "input", 'inputType': "password", 'name': "password_repeat", 'placeholder': "Повторите пароль"},
            ],
            token: "",
            fields: {},
            errors: {},
        }
    },

    mounted() {
        let token = ""
        if (this.$route.query.email_confirm_token) {
            token = this.$route.query.email_confirm_token
        }
        this.token = token
    },

    methods: {
        async submitPwRecovery() {
            const resp = await this.$axios.$post('/api/pw_update', {token: this.token, fields: this.fields})
            console.log(resp)
            if (resp.status){
                this.$auth.loginWith('local', {data: resp.user_info})
                .then((resp) => {
                    this.$auth.setUserToken(resp.data.tokens.access_token, resp.data.tokens.refresh_token)
                })
            }
            else {
                this.errors = resp.errors
            }
        },
        clearError(name) {
            this.errors[name] = ""
        },
    }
}
</script>

<style scoped>
.header {
	text-align: center;
	color: black;
	font-size: 16px;
	font-weight: 700;
	text-transform: uppercase;
}
</style>