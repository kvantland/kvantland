<template>
    <div>
        <SendToEmailForm v-if="checkEmailMode" :title="'Подтверждение адреса электронной почты'" :email="fieldsValueInfo.email" />
        <Form v-else>
            <p class="header"> Личный кабинет </p>
            <form method="post" id="acc" @submit.prevent="submitAccForm">
                <FieldsArea>
                    <FormField v-for="fieldInfo in fieldsTypeInfo" :fieldInfo="fieldInfo" 
                        :key="fieldInfo.name" v-model="fieldsValueInfo[fieldInfo.name]" />
                </FieldsArea>
                <UserAgreement />
                <SubmitButton> Сохранить </SubmitButton>
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
            fieldsTypeInfo: [],
            checkEmailMode: false
        }
    },

    async fetch() {
        const fieldsTypeInfoData = await this.$axios.$get('/api/acc_fields')
        this.fieldsTypeInfo = fieldsTypeInfoData
        console.log(this.fieldsTypeInfo)
    },

    computed: {
        fieldsValueInfo(){
            let fieldsValueInfo = {}
            for (let key in this.$auth.user) {
                fieldsValueInfo[key] = this.$auth.user[key]
            }
            console.log(fieldsValueInfo)
            return fieldsValueInfo
        }
    },

    methods: {
        async submitAccForm() {
            let requestBody = this.fieldsValueInfo
            let emailChanged = false
            await this.$axios.post('/api/update_user_info', requestBody)
                .then((res) => {
                    if (res.data.email_changed)
                        emailChanged = true
                })
            this.checkEmailMode = emailChanged
        }
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