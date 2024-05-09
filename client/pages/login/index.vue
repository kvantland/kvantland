<template>
    <div class="formBackground">
        <AuthForm v-if="mode=='auth'" @changeMode="changeMode" :loginFields="loginFields" />
        <RegForm v-else-if="mode=='reg'" @changeMode="changeMode" :regFields="regFields" />
    </div>
</template>

<script>
import AuthForm from "../../modules/login-page/AuthForm/AuthForm.vue"
import RegForm from "../../modules/login-page/RegForm/RegForm.vue"

export default {
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
        const loginFieldsData = await $axios.$get('/login_fields')
        const regFieldsData = await $axios.$get('/registration_fields')
        return { loginFields: loginFieldsData, regFields: regFieldsData }
    },

    methods: {
        changeMode(modeToChange) {
            console.log(modeToChange)
            this.mode = modeToChange
        }
    }
}
</script>

<style>
form {
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
}
.formBody {
    -webkit-user-select: none;
    user-select: none;
    display: inline-flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px;
    gap: 21px;
    background: white;
    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.10);
    border-radius: 20px;
    align-items: center;
    margin: 0 auto;
    margin-bottom: 100px;
}
.formBackground{
    width: 100%;
    margin-top: 152px;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    display: inline-flex;
    background-color: #D2E8E9;
}
body {
    background-color: #D2E8E9;
}
</style>