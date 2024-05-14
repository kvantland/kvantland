<template>
    <Form>
        <FormHeader mode="reg" @changeHeaderMode="changeHeaderMode" />
        <form method="post" :id="id" @submit.prevent="onSubmitRegForm">
            <FieldsArea>
                <FormField v-for="field in regFields" :fieldInfo="field" :key="field.name" v-model="fields[field.name]" />
            </FieldsArea>
            <UserAgreement v-model="fields['approval']" />
            <Captcha />
            <hr size="1" style="border-width: 1px"/>
            <SubmitButton :form="id"> Зарегистрироваться </SubmitButton>
        </form>
    </Form>
</template>


<script>
import FormHeader from './components/FormHeader'
import UserAgreement from './components/UserAgreement'

export default {
    data() {
        return {
            id: 'reg',
            fields: {},
        }
    },

    props: ['regFields'],

    components: {
        FormHeader,
        UserAgreement,
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
            this.field.recaptcha_token = token
            this.$axios.post('/api/checkout_reg', this.fields)
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