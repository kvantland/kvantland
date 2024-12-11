<template>
	<div>
		<div class="content_wrapper_land">
			<Breadcrumbs :crumbs="landCrumbs" />
			<LandMap />
		</div>
	</div>
</template>


<script>
import LandMap from '~/modules/land-page/LandMap.vue';
export default {
	
	components: {
		LandMap,
	},

	middleware: 'full-auth',

	data() {
		return {
			landCrumbs: {},
		}
	},

	async fetch() {
		const landCrumbsData = await this.$axios.$get('/api/land_crumbs')
		this.landCrumbs = landCrumbsData
	},

	head() {
		return {
			title: 'Квантландия'
		};
	},	
};
</script>

<style scoped>
.content_wrapper_land {
	width: 100%;
	padding-bottom: 80px;
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 40px;
	display: inline-flex;
}
</style>
