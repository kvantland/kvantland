<template>
	<div class="content_wrapper">
		<CurrentEventsSection />
		<MainInfoSection />
		<TournamentInfoSection />
		<KvantlandTeamInfoSection />
		<ContactsSection />
	</div>
</template>

<script>
import MainInfoSection from '~/modules/start-page/MainInfoSection.vue';
import TournamentInfoSection from '~/modules/start-page/TournamentInfoSection.vue';
import KvantlandTeamInfoSection from '~/modules/start-page/KvantlandTeamInfoSection.vue';
import ContactsSection from '~/modules/start-page/ContactsSection.vue';
import CurrentEventsSection from '~/modules/start-page/CurrentEventsSection.vue';

export default {
	components: {
		CurrentEventsSection,
		MainInfoSection,
		TournamentInfoSection,
		KvantlandTeamInfoSection,
		ContactsSection,
	},
	layout: "main-start-page",
	head() {
		return {
			title: "Квантландия"
		}
	},
	
}
</script>

<style scoped>
.content_wrapper {
	padding-bottom: 70px;
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 60px;
	display: inline-flex;
	width: 100%;
}
@media(max-width: 801px) {
	.content_wrapper {
		gap: 24px;
		padding: 0;
	}
}
</style>