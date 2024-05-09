<template>
    <div class="formBody">
        <FormHeader mode="reg" @changeMode="changeHeaderMode" />
        <form method="post" id="id" @submit.prevent="onSubmitRegForm">
            <FormField v-for="field in regFields" :fieldInfo="field" :key="field.name"/>
        </form>
        <div class="buttonArea">
            <UserAgreement />
            <Captcha />
            <hr size="1" style="border-width: 1px"/>
            <SubmitButton :form="id" @onClick="checkCaptcha"> Зарегистрироваться </SubmitButton>
        </div>
    </div>
</template>


<script>
import FormHeader from './components/FormHeader'
import UserAgreement from './components/UserAgreement'

export default {
    data() {
        return {
            id: 'reg',
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
        async checkCaptcha() {
            try {
                const token = await this.$recaptcha.getResponce()
                console.log('ReCaptcha token:', token)
                await this.$recaptcha.reset()
            }
            catch (error) {
                console.log('Login error', error)
            }
        }
    }
}
</script>