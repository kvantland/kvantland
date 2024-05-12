<template>
	<div class="check_cont">
        <input class="checkbox" type="checkbox" name="approval"
            id="approval" v-model="check"required />
        <div class="label"> Я принимаю условия <NuxtLink to="/policy"> <span class="underline">Политики конфиденциальности</span> </NuxtLink> и даю <span class="underline approval"> согласие
            на обработку своих персональных данных</span>
        </div>
	</div>
</template>

<script>
export default {
    data() {
        return {
            value: false,
        }
    },
    computed: {
        check: {
            get() {
                return this.value
            },
            set(val) {
                this.$emit('input', val)
            }
        }
    }
}
</script>

<style>
.check_cont {
	display: inline-flex;
	justify-content: space-between;
	align-items: center;
	font-size: 12px;
	color: rgba(0, 0, 0, 0.60);
	font-weight: 500;
	width: 320px;
}

.check_cont input.checkbox {
	-webkit-appearance: none;
	appearance: none;
	border: 1px #99BBFF solid;
	border-radius: 4px;
	background: #FBFBFD;
	width: 28px;
	height: 28px;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
}

.check_cont input.checkbox:checked:after {
	content: '✔️';
	color:white;
}

.check_cont .label {
	width: 270px;
}

.check_cont span.underline {
	cursor: pointer;
}

span.underline {
    text-decoration: underline;
}
</style>