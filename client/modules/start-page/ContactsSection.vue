<script>
import ContactsArea from '../index-page/ContactsArea/ContactsArea.vue';
export default {
	components: {
		ContactsArea,
	},
	data() {
		return {
			contacts: [
				{
					'id': "vk",
					'image': "vk.svg",
					'source_link': "https://vk.com/kvantland"
				},
				
				{
					'id': "telegram",
					'image': "tg.svg",
					'source_link': "https://t.me/kvantland"
				},
				
				{
					'id': "youtube",
					'image': "play.svg",
					'source_link': "https://www.youtube.com/@Kvantland"
				},
				
				{
					'id': "email",
					'image': "email.svg",
					'source_link': "mailto:" + "support@kvantland.com"
				}
			]
		}
	}
}
</script>

<template>
	<section id="ContactsSection">
		<ContactsArea :contacts="contacts" />
	</section>
</template>