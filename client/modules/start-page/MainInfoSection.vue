<template>
	<section id="MainInfoSection">
		<CommonInfo  :info-cards="infoCards" title="О нас" />
	</section>
</template>

<script>
import CommonInfo from '../index-page/CommonInfo/CommonInfo.vue';

export default {
	components: {
		CommonInfo,
	},
	data() {
		return {
			infoCards: [
				{
					image: "people.svg",
					desc: `<span class="bold_text">Мы – команда</span> авторов журнала “Квантик”, программистов, 
								художников и редакторов, популяризаторов математики и информатики. Проводим
								онлайн-турниры с интерактивными задачами для детей и взрослых на этом сайте. `,

				},

				{
					image: "screen.svg",
					desc:  `<span class="bold_text">Каждый турнир это смесь олимпиады и компьютерной игры.</span> 
									Участие бесплатное, а победителей ждут призы! Турниры индивидуальные. Для участия 
									достаточно выбрать турнир на этом сайте и зарегистрироваться.`
				},
							
				{
					image: "planet.svg",
					desc: `<span class="bold_text">Примерно 3500 детей и взрослых из разных стран</span> 
								(Австралия, Болгария, Сербия, Россия, Казахстан, США, Белоруссия 
								и других) уже поучаствовали в турнирах. Давайте побьём этот рекорд вместе!`
				},
    	]
		}
	}
}
</script>