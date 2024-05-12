<template>
    <Form>
        <FormHeader mode="auth" @changeHeaderMode="changeHeaderMode" />
        <form method="post" :id="id" @submit.prevent="onSubmitAuthForm">
            <FieldsArea>
                <FormField v-for="field in loginFields" :fieldInfo="field" 
                :key="field.name" v-model="fields[field.name]" />
            </FieldsArea>
            <SubmitButton :form="id"> Войти </SubmitButton>
        </form>
            <hr size="1" style="border-width: 1px" />
            <VkAuthButton />
            <NuxtLink to="/pw_recovery" class="pwRecoveryLink">
                Восстановить пароль
            </NuxtLink>
        </Form>
</template>

<script>
import FormHeader from './components/FormHeader'

export default {
    props: ['loginFields'],

    data() {
        return {
            id: 'login',
            fields: {},
        }
    },

    components: {
        FormHeader,
    },

    methods: {
        changeHeaderMode(modeToChange) {
            this.$emit('changeHeaderMode', modeToChange)
        },
        async onSubmitAuthForm() {
            console.log('auth!')
            await this.$auth.loginWith('local', {data:this.fields})
            .then((res) => {
                this.$auth.setUserToken(res.data.tokens.access_token, res.data.tokens.refresh_token)
                this.$auth.setUser(res.data.user)
            })
        },
    }
}
</script>

<style>
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