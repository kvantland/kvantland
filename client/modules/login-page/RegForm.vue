<template>
    <div>
        <SendToEmailForm
			v-if="checkEmailMode" :title="'Регистрация'" :email="fields.email"
            :description="sendEmailDescription" :form-data="sendEmailData" :api-request-url="sendEMailRequestUrl"/>
        <Form v-else>
            <FormHeader mode="reg" @changeHeaderMode="changeHeaderMode" />
            <form :id="id" method="post" @submit.prevent="onSubmitRegForm">
                <FieldsArea>
                    <FormField
						v-for="field in regFields" :key="field.name" v-model="fields[field.name]" 
                        :field-info="field" :error="errors[field.name]" @clearError="clearRegError"/>
                </FieldsArea>
                <UserAgreement v-model="fields.approval" :error="errors.approval" @clearError="clearRegError"/>
                <Captcha :error="errors['captcha']" style="align-self: center;"/>
                <hr size="1" style="border-width: 1px"/>
                <SubmitButton :form="id"> Зарегистрироваться </SubmitButton>
            </form>
        </Form>
    </div>
</template>


<script>
import FormHeader from './components/FormHeader'

export default {

    components: {
        FormHeader,
    },

    props: {
        regFields: {},
        errors: {default: {}},
    },
    data() {
        return {
            id: 'reg',
            fields: {},
            checkEmailMode: false,
            sendEmailDescription: `Письмо для подтверждения регистрации</br> успешно 
                                    отправлено на Ваш адрес!</br> Для подтверджения адреса 
                                    перейдите</br> по ссылке в письме, которое придёт 
                                    Вам<br/> на почту`,
            sendEmailData: {},
            sendEMailRequestUrl: "/api/send_reg_message_again",
        }
    },

    async mounted() {
        try {
            await this.$recaptcha.init()
        }
        catch(e) {
            console.log(e)
        }
    },

    methods: {
        changeHeaderMode(modeToChange) {
            this.$emit('changeHeaderMode', modeToChange)
        },
        clearRegError(name) {
            const errors = this.errors ? this.errors : {}
            errors[name] = ""
            this.$emit('updateErrors', errors)
        },
        async onSubmitRegForm() {
            let token
            try {
                token = await this.$recaptcha.getResponse()
                await this.$recaptcha.reset()
            }
            catch (error) {
                console.log('Login error:', error)
            }
            let errors, status, infoFields, sendEmailData

            infoFields = this.fields
            this.regFields.forEach((field) => {if (!infoFields[field.name]) infoFields[field.name] = ""})
            if (!infoFields.approval) infoFields.approval = false

            sendEmailData = {'user': infoFields, 'captcha': token}
            await this.$axios.$post('/api/checkout_reg', sendEmailData)
                .then((res) => {
                        errors = res.errors
                        status = res.status
                    })
            console.log(errors)
            this.$emit('updateErrors', errors)
            if (status) {
                this.checkEmailMode = true
                this.sendEmailData = sendEmailData
            }
        },
    },
}
</script>

<style scoped>
</style>