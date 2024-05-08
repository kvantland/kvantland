<template>
    <div class="contacts_area" id="contacts">
        <p class="page_header"> Будем на связи </p>
        <p class="text"> В наших социальных сетях мы регулярно публикуем 
                        интересные новости о проекте, анонсы ближайших событий и 
                        нестандартные задачки для всех!  </br></br>  
                        Присоединяйтесь и будете всегда в курсе событий! </p>
        <div class="button_area">
            <ContactButton v-for="contact in contacts" :contactInfo="contact" :key="contact.id"/>
        </div>
            <p> Адрес техподдержки: 
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

    data() {
        return {
            contacts: {},
        }
    },

    computed: {
        supportEmail() {
            let email = this.contacts.filter((contact) => contact.id == 'email')[0].source_link
            return { link: email, title: email.split(':')[1]}
        },
    },

    async fetch() {
        const contactsData = await this.$axios.$get('/contacts')
        this.contacts = contactsData
    }
}
</script>