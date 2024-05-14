<template>
    <AuthForm v-if="mode=='auth'" @changeHeaderMode="changeHeaderMode" :loginFields="loginFields" />
    <RegForm v-else-if="mode=='reg'" @changeHeaderMode="changeHeaderMode" :regFields="regFields" />
</template>

<script>
import AuthForm from "../modules/login-page/AuthForm.vue"
import RegForm from "../modules/login-page/RegForm.vue"

export default {
    layout: 'forms',
    
    components: {
        AuthForm,
        RegForm,
    },
    data() {
        return {
            mode: 'auth'
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
        }
    }
}
</script>