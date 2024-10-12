<template>
    <div class="support_area">
        <p>Если возникли технические проблемы, напишите в нашу службу поддержки</p>
        <a class="border" :href="supportEmail.supportLink" target="_blank">
            <div class="button">{{ supportEmail.title }}</div>
        </a>
    </div>
</template>

<script>
export default {
    data() {
        return {
            supportEmail: ''
        }
    },

    async fetch() {
        const contactsInfo = await this.$axios.$get('/api/contacts')
        let supportEmail = {'link': '', 'title': ''}
        for (const contact of contactsInfo) {
            if (contact.id == 'email') {
                supportEmail.supportLink = contact.source_link
                supportEmail.title = contact.source_link.split(':')[1]
            }
        }
        this.supportEmail = supportEmail
    }
}
</script>

<style scoped>
.support_area {
	padding: max(20px, min(3vw, 40px));
	border-radius: 20px;
	overflow: hidden;
	border: 3px #1E8B93 solid;
	justify-content: flex-start;
	align-items: center;
	gap: 40px; display: inline-flex;
	align-self: stretch;
}

.support_area p {
	flex: 1 1 0;
	color: black;
	font-size: max(15px, min(2vw, 24px));
	font-family: Montserrat;
	font-weight: 500;
	word-wrap: break-word;
}

.support_area .border {
	padding: 10px 40px;
	background: #1E8B93;
	box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25);
	border-radius: 10px;
	overflow: hidden;
	justify-content: center;
	align-items: center;
	gap: 10px;
	display: flex;
}

.support_area .button {
	color: white;
	font-size:  max(15px, min(2vw, 24px));
	font-family: Montserrat Alternates;
	font-weight: 600;
	word-wrap: break-word;
}
@media(max-width: 800px) {
	.support_area {
		border-radius: 8px;
		padding: 16px;
		gap: 10px;
		font-size: 12px;
		flex-direction: column;
	}
	.support_area .border {
		width: 100%;
		box-sizing: border-box;
	}
}
</style>