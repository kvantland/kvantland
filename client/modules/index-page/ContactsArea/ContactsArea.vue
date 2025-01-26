<template>
    <div id="contacts" class="contacts_area">
        <p class="page_header"> Будем на связи </p>
        <p class="text"> В наших социальных сетях мы регулярно публикуем 
                        интересные новости о проекте, анонсы ближайших событий и 
                        нестандартные задачки для всех!  </br></br>  
                        Присоединяйтесь и будете всегда в курсе событий! </p>
        <div class="button_area">
            <ContactButton v-for="contact in contacts" :key="contact.id" :contact-info="contact"/>
        </div>
            <p class="text"> Адрес техподдержки: 
                <NuxtLink  to="supportEmail.link" target="_blank"> {{ supportEmail.title }} </NuxtLink>
            </p>
    </div>
</template>

<script>
import ContactButton from "./components/ContactButton.vue"

export default {
    
    components: {
        ContactButton,
    },
    props: ['contacts'],

    computed: {
        supportEmail() {
            try {
                const email = this.contacts.filter((contact) => contact.id === 'email')[0].source_link
                return { link: email, title: email.split(':')[1]}
            }
            catch {
                return { link: '', title: '' }
            }
        },
    },
}
</script>

<style scoped>
.contacts_area {
	flex-direction: column; 
	justify-content: flex-start; 
	align-items: flex-start; 
	gap: 40px; 
	display: flex;
}

.page_header {
	color: #1E8B93;
	font-size: 40px;
	font-family: Montserrat Alternates;
	font-weight: 600;
}

.contacts_area .text {
	color: black; 
	font-size: min(2vw, 20px); 
	font-weight: 400;
}

.contacts_area .button_area {
	justify-content: flex-start; 
	align-items: flex-start; 
	gap: 40px; 
	display: inline-flex;
    width: 100%;
} 
@media(max-width: 800px) {
	.contacts_area .button_area {
		gap: 2vw;
	}
	.page_header {
		font-size: 24px;
	}
	.contacts_area {
		gap: 16px;
	}
	.contacts_area .text {
		font-size: 14px;
	}
}
</style>