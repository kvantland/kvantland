<template>
    <AuthForm v-if="mode=='auth'" @changeHeaderMode="changeHeaderMode" 
        @updateErrors="updateLoginInfo" :loginFields="loginFields" :errors="loginErrors" />
    <RegForm v-else-if="mode=='reg'" @changeHeaderMode="changeHeaderMode" 
        @updateErrors="updateRegInfo" :regFields="regFields" :errors="regErrors"/>
</template>

<script>
import AuthForm from "../../modules/login-page/AuthForm.vue"
import RegForm from "../../modules/login-page/RegForm.vue"

export default {
    layout: 'forms',
    
    components: {
        AuthForm,
        RegForm,
    },

    head() {
        return {
            title: 'Квантандия - авторизация',
        }
    },

    data() {
        return {
            mode: 'auth',
            regErrors: "",
            loginErrors: "",
        }
    },

    async asyncData({$axios}) {
        const loginFieldsData = await $axios.$get('/api/login_fields')
        const regFieldsData = await $axios.$get('/api/registration_fields')
        return { loginFields: loginFieldsData, regFields: regFieldsData }
    },

    methods: {
        changeHeaderMode(modeToChange) {
            console.log(modeToChange)
            this.mode = modeToChange
        },
        updateLoginInfo(info) {
            this.loginErrors = info
        },
        updateRegInfo(info) {
            this.regErrors = info
            console.log(this.regErrors)
        }
    },
}
</script>