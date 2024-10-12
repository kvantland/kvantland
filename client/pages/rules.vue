<template>
	<div class="content_wrapper_rules">
		<Breadcrumbs :crumbs="rulesCrumbs" />
		<RulesInfo />
	</div>
</template>


<script>
import RulesInfo from '../modules/rules-page/RulesInfo.vue'
	export default {
		components: {
			RulesInfo,
		},
		middleware: 'auth',

		data() {
			return {
				rulesCrumbs: {},
			}
		},

	async fetch() {
		const rulesCrumbsData = await this.$axios.$get('/api/rules_crumbs')
		this.rulesCrumbs = rulesCrumbsData
	},
		head() {
			return {
				title: 'Правила — Квантландия'
			};
		},
};
</script>

<style scoped>
.content_wrapper_rules {
	width: 100%;
	padding: 0 min(80px, 5vw);
	margin-top: 130px;
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 40px;
	display: inline-flex;
	padding-bottom: 80px;
}
@media(max-width: 800px) {
	.content_wrapper_rules {
		gap: 24px;
		padding: 16px;
		margin-top: 80px;
	}
}
</style>
