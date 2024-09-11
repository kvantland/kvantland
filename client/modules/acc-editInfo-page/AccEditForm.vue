<template>
	<Form>
		<p class="header"> Редактирование данных </p>
		<form method="post" id="acc" @submit.prevent="submitAccForm">
			<FieldsArea>
				<div class="global_error" v-if="globalError">
					<img class="error_img" src="/icons/info.svg" />
					<p class="error" v-html="globalError"> </p>
				</div>
				<FormField v-for="fieldInfo in fieldsTypeInfo" v-model="fieldsValueInfo[fieldInfo.name]" :fieldInfo="fieldInfo" 
					@clearError="clearError(fieldInfo.name)"
					:key="fieldInfo.name"  :error="fieldsErrors[fieldInfo.name]" />
			</FieldsArea>
			<UserAgreement v-model="fieldsValueInfo.approval" :error="fieldsErrors.approval"  @clearError="clearError('approval')" />
			<SubmitButton :id="'acc'"> Сохранить </SubmitButton>
			<hr size="1">
			<BackButton />
		</form>
	</Form>
</template>

<script>
export default {
	props: {
		fieldsTypeInfo: {
			type: Array,
			default: () => {return []}
		},
		startFieldsValueInfo: {
			type: Object,
			default: () => {return {}}
		},
		globalError: {
			type: String,
			default: ""
		},
		fieldsErrors: {
			type: Object,
			default: () => {return {}}
		}
	},

	data() {
		return {
			fieldsValueInfo: JSON.parse(JSON.stringify(this.startFieldsValueInfo)),
		}
	},

	methods: {
		clearError(name) {
			this.$emit('clearError', name)
		},
		submitAccForm(){
			this.$emit('submitAccForm', this.fieldsValueInfo)
		}
	}
	
}
</script>

<style scoped>
.header {
    display: inline-flex;
    justify-content: center;
    gap: 20px;
    font-weight: 700;
    font-size: 16px;
    text-transform: uppercase;
}

.error{
	align-self: flex-start;
	color: #B62C5A;
	font-size: 12px;
	font-weight: 600;
}

.error_img {
    align-self: center !important;
	width: 16px;
	height: 16px;
}

.global_error {
    gap: 16px;
    display: inline-flex;
    align-self: stretch;
}
</style>