<template>
    <div>
        <SendToEmailForm v-if="checkEmailMode" :title="'Подтверждение адреса электронной почты'" :email="fieldsValueInfo.email" 
            :description="sendEmailDescription" :formData="sendEmailData" :apiRequestUrl="sendEMailRequestUrl"/>
        <Form v-else>
            <p class="header"> Редактирование данных </p>
            <form method="post" id="acc" @submit.prevent="submitAccForm">
                <FieldsArea>
                    <div class="global_error" v-if="globalError">
                        <img class="error_img" src="/icons/info.svg" />
                        <p class="error" v-html="globalError"> </p>
                    </div>
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

    head() {
        return {
            title: ' Личный кабинет — Квантландия '
        }
    },

    data() {
        return {
            pageMod: 'updateInfo',
            fieldsTypeInfo: [],
            fieldsValueInfo: [],
            fieldsErrors: {},
            globalError: "",
            checkEmailMode: false,
            sendEmailDescription: `Письмо для подтверждения адреса
                                    электронной почты,</br> 
                                    привязанной	к Вашему аккаунту, успешно отправлено!</br>
                                    Для подтверждения адреса, перейдите по ссылке в</br>
                                    письме, которое придёт Вам на почту`,
            sendEmailData: {},
            sendEMailRequestUrl: "/api/acc_form_request",
        }
    },

    async fetch() {
        let fieldsTypeInfoData = await this.$axios.$get('/api/acc_fields')
        this.fieldsTypeInfo = fieldsTypeInfoData
    },

    mounted() {
        let fieldsValueInfo = {}
        switch (this.$route.query.request) {
            case "oauthReg": {
                for (let key in JSON.parse(this.$route.query.user_info)) {
                    fieldsValueInfo[key] = JSON.parse(this.$route.query.user_info)[key]
                }
                this.pageMod = "oauthReg"
                break;
            }
            default: {
                for (let key in this.$auth.user) {
                    fieldsValueInfo[key] = this.$auth.user[key]
                }
                break;
            }
        }
        this.fieldsValueInfo = fieldsValueInfo
        switch(this.$route.query.globalError) {
            case 'fillFields':
                this.globalError = "Все поля в личном кабинете обязательны </br> для заполнения"
        }
    },

    methods: {
        clearError(name) {
            this.fieldsErrors[name] = ""
            this.globalError = ""
        },
        async submitAccForm() {
            let userInfo = this.fieldsValueInfo
            this.fieldsTypeInfo.forEach((field) => {if (!userInfo[field.name]) userInfo[field.name] = ""})
            if (!userInfo['approval']) userInfo['approval'] = false
            const requestBody = {'user_info': userInfo, 'action_type': this.pageMod}
            let emailChanged = false
            let errors = {}
            let status = false
            await this.$axios.$post('/api/acc_form_request', requestBody)
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

<style scoped>
.header {
    display: inline-flex;
    justify-content: center;
    gap: 20px;
    font-weight: 700;
    font-size: 16px;
    text-transform: uppercase;
}

.error{
	align-self: flex-start;
	color: #B62C5A;
	font-size: 12px;
	font-weight: 600;
}

.error_img {
    align-self: center !important;
	width: 16px;
	height: 16px;
}

.global_error {
    gap: 16px;
    display: inline-flex;
    align-self: stretch;
}
</style>