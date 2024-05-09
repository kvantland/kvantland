<template>
    <div class="formBody">
        <FormHeader mode="reg" @changeMode="changeMode" />
        <form method="post" id="id">
            <FormField v-for="field in regFields" :fieldInfo="field" :key="field.name"/>
        </form>
        <div class="buttonArea">
            <UserAgreement />
            <Captcha />
            <hr size="1" style="border-width: 1px"/>
            <SubmitButton :form="id"> Зарегистрироваться </SubmitButton>
        </div>
    </div>
</template>


<script>
import SubmitButton from '../../../UI/SubmitButton.vue'
import FormField from '../../../UI/FormField/FormField.vue'
import Captcha from '../../../UI/Captcha.vue'
import FormHeader from '../components/FormHeader'
import UserAgreement from '../components/UserAgreement'

export default {
    data() {
        return {
            id: 'reg',
        }
    },

    props: ['regFields'],

    components: {
        SubmitButton,
        FormField,
        FormHeader,
        Captcha,
        UserAgreement,
    },

    methods: {
        changeMode(modeToChange) {
            this.$emit('changeMode', modeToChange)
        }
    }
}
</script>