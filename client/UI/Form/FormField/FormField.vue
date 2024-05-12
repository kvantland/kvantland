<template>
    <div class="field">
        <div class="content">
            <span class="placeholder"> {{ fieldInfo.placeholder }} </span>
            <input :name="fieldInfo.name" :type="fieldInfo.inputType" v-if="fieldInfo.type=='input'" 
            @input="$emit('input', $event.target.value)" required />
            <SelectField v-else-if="fieldInfo.type=='select'" @selectOption="selectOption" :fieldInfo="fieldInfo" />
        </div>
    </div>
</template>

<script>
import SelectField from './components/SelectField.vue'

export default {
    components: {
        SelectField,
    },
    props: ['fieldInfo'],
    methods: {
        selectOption(option){
            this.$emit('input', option)
        }
    }
}
</script>

<style>
.field {
    display: inline-flex;
    justify-content: space-between;
    padding: 10px 20px;
    background: rgba(26.35, 88.38, 102, 0.10);
    border-radius: 6px;
    width: 280px;
    gap: 2px;
}
.field .placeholder {
    color: rgba(0, 0, 0, 0.60);
    font-size: 10px;
    font-weight: 400;
}
.field input {
    font-size: 12px;
    font-weight: 600;
    background-color: transparent;
    border: none;
    font-family: Montserrat;
}
.field input[type="password"] {
    font-weight: 400 !important;
}
input:-webkit-autofill {
    background: none;
}
.field .content {
    display: inline-flex;
    flex-direction: column;
    gap: 2px;
    width: 100%;
}
.field input:focus {
	outline: none;
}
</style>