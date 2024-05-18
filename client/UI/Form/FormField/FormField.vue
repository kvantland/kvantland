<template>
    <div class="fieldWithError">
        <div class="field">
            <div class="content">
                <span class="placeholder"> {{ fieldInfo.placeholder }} </span>
                <input :name="fieldInfo.name" :type="fieldInfo.inputType" v-if="fieldInfo.type=='input'" 
                @input="changeValue($event.target.value)" :value="value" required :readonly="readonly" />
                <SelectField v-else-if="fieldInfo.type=='select'" @selectOption="selectOption" 
                    :fieldInfo="fieldInfo" :selectedOption="currentValue" />
            </div>
            <img v-if="error" class="error_img" src="/icons/info.svg" />
        </div>
        <p class="error" v-if="error"> {{ error }} </p>
    </div>
</template>

<script>
import { readonly } from 'vue';
import SelectField from './components/SelectField.vue'

export default {
    components: {
        SelectField,
    },

    props: {
        fieldInfo:{},
        value:{default: ""},
        readonly:{default: false},
        error:{default: ""},
    },

    computed: {
        currentValue: {
            get() {
                return this.value
            },
            set(newValue) {}
        }
    },

    methods: {
        selectOption(option){
            this.error=""
            this.currentValue = option
            this.$emit('input', option)
        },
        changeValue(newValue){
            this.error = ""
            this.$emit('input', newValue)
        }
    },
}
</script>

<style>
.fieldWithError {
    display: inline-flex;
    flex-direction: column;
    gap: 2px;
}
.field {
    display: inline-flex;
    justify-content: space-between;
    padding: 10px 20px;
    background: rgba(26.35, 88.38, 102, 0.10);
    border-radius: 6px;
    min-width: 280px;
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
.error{
    padding: 0 20px;
	align-self: flex-start;
	color: #B62C5A;
	font-size: 12px;
	font-weight: 600;
}

.error_img {
    align-self: center;
	width: 16px;
	height: 16px;
}
</style>