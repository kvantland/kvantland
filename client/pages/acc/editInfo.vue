<template>
    <div>
        <SendToEmailForm v-if="checkEmailMode" :title="'Подтверждение адреса электронной почты'" :email="fieldsValueInfo.email" 
            :description="sendEmailDescription" :formData="sendEmailData" :apiRequestUrl="sendEMailRequestUrl"/>
        <Form v-else>
            <p class="header"> Личный кабинет </p>
            <form method="post" id="acc" @submit.prevent="submitAccForm">
                <FieldsArea>
                    <FormField v-for="fieldInfo in fieldsTypeInfo" :fieldInfo="fieldInfo" @clearError="clearError"
                        :key="fieldInfo.name" v-model="fieldsValueInfo[fieldInfo.name]" :error="fieldsErrors[fieldInfo.name]" />
                </FieldsArea>
                <UserAgreement :error="fieldsErrors.approval" v-model="fieldsValueInfo['approval']" @clearError="clearError" />
                <SubmitButton :id="'acc'"> Сохранить </SubmitButton>
                <hr size="1">
                <BackButton />
            </form>
        </Form>
    </div>
</template>

<script>
export default {
    layout: "forms",
    middleware: "auth",

    head() {
        return {
            title: ' Личный кабинет — Квантландия '
        }
    },

    data() {
        return {
            fieldsTypeInfo: [],
            fieldsValueInfo: [],
            fieldsErrors: {},
            checkEmailMode: false,
            sendEmailDescription: `Письмо для подтверждения адреса
                                    электронной почты,</br> 
                                    привязанной	к Вашему аккаунту, успешно отправлено!</br>
                                    Для подтверждения адреса, перейдите по ссылке в</br>
                                    письме, которое придёт Вам на почту`,
            sendEmailData: {},
            sendEMailRequestUrl: "/api/send_acc_message_again",
        }
    },

    async fetch() {
        let fieldsTypeInfoData = await this.$axios.$get('/api/acc_fields')
        this.fieldsTypeInfo = fieldsTypeInfoData
    },

    mounted() {
        let fieldsValueInfo = {}
        for (let key in this.$auth.user) {
            fieldsValueInfo[key] = this.$auth.user[key]
        }
        this.fieldsValueInfo = fieldsValueInfo
    },

    methods: {
        clearError(name) {
            this.fieldsErrors[name] = ""
        },
        async submitAccForm() {
            let userInfo = this.fieldsValueInfo
            this.fieldsTypeInfo.forEach((field) => {if (!userInfo[field.name]) userInfo[field.name] = ""})
            if (!userInfo['approval']) userInfo['approval'] = false
            const requestBody = {'user_info': userInfo}
            let emailChanged = false
            let errors = {}
            let status = false
            await this.$axios.$post('/api/update_user_info', requestBody)
                .then((res) => {
                    status = res.status
                    if (res.email_changed)
                        emailChanged = true
                    errors = res.errors
                })
            console.log(errors)
            this.fieldsErrors = errors
            if (status) {
                this.checkEmailMode = emailChanged
                this.sendEmailData = requestBody
            }
        },
    }

}
</script>

<style>
.header {
    display: inline-flex;
    justify-content: center;
    gap: 20px;
    font-weight: 700;
    font-size: 16px;
    text-transform: uppercase;
}
</style>
</template>