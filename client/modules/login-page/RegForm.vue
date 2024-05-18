<template>
    <div>
        <SendToEmailForm v-if="checkEmailMode" :title="'Подтверждение адреса электронной почты'" :email="fields.email" />
        <Form v-else>
            <FormHeader mode="reg" @changeHeaderMode="changeHeaderMode" />
            <form method="post" :id="id" @submit.prevent="onSubmitRegForm">
                <FieldsArea>
                    <FormField v-for="field in regFields" :fieldInfo="field" :key="field.name" 
                        v-model="fields[field.name]" :error="errors[field.name]"/>
                </FieldsArea>
                <UserAgreement />
                <Recaptcha />
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
                console.log('ReCaptcha token:', token)
                await this.$recaptcha.reset()
            }
            catch (error) {
                console.log('Login error', error)
            }
            let errors = {}
            await this.$axios.post('/api/checkout_reg', {'user': this.fields, 'captcha': token})
                .then((res) => {
                        errors = res.data.errors
                    })
            console.log(errors)
            this.$emit('updateErrors', errors)
            this.checkEmailMode = true
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