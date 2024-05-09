<template>
    <div class="formBody">
        <FormHeader mode="auth" @changeMode="changeMode" />
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
import SubmitButton from '../../../UI/SubmitButton.vue'
import FormField from '../../../UI/FormField/FormField.vue'
import FormHeader from '../components/FormHeader'
import VkAuthButton from '../../../UI/VkAuthButton.vue'

export default {
    props: ['loginFields'],

    data() {
        return {
            id: 'login',
        }
    },

    components: {
        SubmitButton,
        FormField,
        VkAuthButton,
        FormHeader,
    },

    methods: {
        changeMode(modeToChange) {
            this.$emit('changeMode', modeToChange)
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