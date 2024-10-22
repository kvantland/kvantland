<template>
    <div>
        <SendToEmailForm
			v-if="checkEmailMode" :title="'Подтверждение адреса электронной почты'" :email="fieldsValueInfo.email" 
            :description="sendEmailDescription" :form-data="sendEmailData" :api-request-url="sendEMailRequestUrl"/>
        <AccEditForm
			v-else :start-fields-value-info="fieldsValueInfo" 
			:fields-type-info="fieldsTypeInfo" :fields-errors="fieldsErrors" 
			@submitAccForm="submitAccForm" @clearError="clearError"></AccEditForm>
    </div>
</template>

<script>
import AccEditForm from '~/modules/acc-editInfo-page/AccEditForm.vue';

export default {
	components: {
		AccEditForm,
	},

    layout: "forms",

	async asyncData({ $axios, route, redirect }) {
        const fieldsTypeInfo = await $axios.$get('/api/acc_fields');
		let fieldsValueInfo
        switch (route.query.request) {
            case 'oauthReg': {
                fieldsValueInfo = JSON.parse(route.query.user_info);
                break;
            }
            default: {
				try {
					fieldsValueInfo = await $axios.$get('/api/user')
				}
				catch {
					return redirect('/login')
				}
				if (!fieldsValueInfo.user) {
                	return redirect('/login');
				}
				else {
					fieldsValueInfo = fieldsValueInfo.user
				}
                break;
            }
        }

        return {
            fieldsTypeInfo,
            fieldsValueInfo,
            globalError: route.query.globalError === 'fillFields'
                ? 'Все поля в личном кабинете обязательны </br> для заполнения'
                : ''
        };
    },

	data() {
        return {
            pageMod: 'updateInfo',
            fieldsErrors: {},
            checkEmailMode: false,
            sendEmailDescription: `Письмо для подтверждения адреса
                                    электронной почты,</br> 
                                    привязанной к Вашему аккаунту, успешно отправлено!</br>
                                    Для подтверждения адреса, перейдите по ссылке в</br>
                                    письме, которое придёт Вам на почту`,
            sendEmailData: {},
            sendEMailRequestUrl: "/api/acc_form_request",
        };
    },

    head() {
        return {
            title: ' Личный кабинет — Квантландия '
        };
    },

    methods: {
        clearError(name='') {
			if (!name) {
				return
			}
			console.log(name)
            this.fieldsErrors[name] = ""
            this.globalError = ""
        },

        async submitAccForm(userInfo) {
            this.fieldsTypeInfo.forEach((field) => {
                if (!userInfo[field.name]) userInfo[field.name] = ""
            })
            if (!userInfo.approval) userInfo.approval = false
            const requestBody = { user_info: userInfo, action_type: this.pageMod }
            let emailChanged = false
            let errors = {}
            let status = false
            await this.$axios.$post('/api/acc_form_request', requestBody)
                .then((res) => {
                    status = res.status
                    if (res.email_changed)
                        emailChanged = true
                    errors = res.errors
                });
            console.log(errors);
            this.fieldsErrors = errors;
            if (status) {
                this.checkEmailMode = emailChanged
                this.sendEmailData = requestBody
            }
        },
    },
};
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