<template>
    <div class="formBody">
        <FormHeader mode="auth" @changeHeaderMode="changeHeaderMode" />
        <form method="post" id="id">
            <FormField v-for="field in loginFields" :fieldInfo="field" :key="field.name"/>
        </form>
        <div class="buttonArea">
            <SubmitButton :form="id"> Войти </SubmitButton>
            <hr size="1" style="border-width: 1px"/>
            <VkAuthButton />
        </div>
        <NuxtLink to="/pw_recovery" class="pwRecoveryLink">
            Восстановить пароль
        </NuxtLink>
    </div>
</template>

<script>
import FormHeader from './components/FormHeader'

export default {
    props: ['loginFields'],

    data() {
        return {
            id: 'login',
        }
    },

    components: {
        FormHeader,
    },

    methods: {
        changeHeaderMode(modeToChange) {
            this.$emit('changeHeaderMode', modeToChange)
        }
    }
}
</script>

<style>
.buttonArea {
    display: inline-flex;
    flex-direction: column;
    align-self: stretch;
    gap: 20px;
}
.pwRecoveryLink {
    display: inline-flex;
    text-decoration: underline;
    color: #1E8B93;
    font-size: 14px;
    font-weight: 500;
    align-self: stretch;
    text-align: right;
    flex-direction: row-reverse;
}
</style>