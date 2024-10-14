<template>
    <AuthForm
		v-if="mode=='auth'" :login-fields="loginFields" 
        :errors="loginErrors" @changeHeaderMode="changeHeaderMode" @updateErrors="updateLoginInfo" />
    <RegForm
		v-else-if="mode=='reg'" :reg-fields="regFields" 
        :errors="regErrors" @changeHeaderMode="changeHeaderMode" @updateErrors="updateRegInfo"/>
</template>

<script>
import AuthForm from "../../modules/login-page/AuthForm.vue"
import RegForm from "../../modules/login-page/RegForm.vue"

export default {
    
    components: {
        AuthForm,
        RegForm,
    },
    layout: 'forms',

    async asyncData({$axios}) {
        const loginFieldsData = await $axios.$get('/api/login_fields')
        const regFieldsData = await $axios.$get('/api/registration_fields')
        return { loginFields: loginFieldsData, regFields: regFieldsData }
    },

    data() {
        return {
            mode: 'auth',
            regErrors: "",
            loginErrors: "",
        }
    },

    head() {
        return {
            title: 'Квантандия - авторизация',
        }
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