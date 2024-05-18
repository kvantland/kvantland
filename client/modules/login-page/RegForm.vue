<template>
    <div>
        <SendToEmailForm v-if="checkEmailMode" :title="'Подтверждение адреса электронной почты'" :email="fields.email"
            :description="sendEmailDescription" :formData="sendEmailData" :apiRequestUrl="sendEMailRequestUrl"/>
        <Form v-else>
            <FormHeader mode="reg" @changeHeaderMode="changeHeaderMode" />
            <form method="post" :id="id" @submit.prevent="onSubmitRegForm">
                <FieldsArea>
                    <FormField v-for="field in regFields" :fieldInfo="field" :key="field.name" 
                        v-model="fields[field.name]" :errorProp="errors[field.name]"/>
                </FieldsArea>
                <UserAgreement />
                <Captcha :error="errors['captcha']"/>
                <hr size="1" style="border-width: 1px"/>
                <SubmitButton :form="id"> Зарегистрироваться </SubmitButton>
            </form>
        </Form>
    </div>
</template>


<script>
import FormHeader from './components/FormHeader'

export default {
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

    props: {
        regFields: {},
        errors: {default: {}},
    },

    components: {
        FormHeader,
    },

    methods: {
        changeHeaderMode(modeToChange) {
            this.$emit('changeHeaderMode', modeToChange)
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
            sendEmailData = {'user': infoFields, 'captcha': token}
            await this.$axios.post('/api/checkout_reg', sendEmailData)
                .then((res) => {
                        errors = res.data.errors
                        status = res.data.status
                    })
            this.$emit('updateErrors', errors)
            if (status) {
                this.checkEmailMode = true
                this.sendEmailData = sendEmailData
            }
        },
    },

    async mounted() {
        try {
            await this.$recaptcha.init()
        }
        catch(e) {
            console.log(e)
        }
    },
}
</script>

<style scoped>
</style>