<template>
	<div>
		<div class="content_wrapper_land">
			<Breadcrumbs :crumbs="crumbs" />
			<LandMap :class-value=classValue />
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

	async asyncData({params, $axios}) {
		const classValue = params.classValue
		let crumbs
		await $axios.$post('/api/breadcrumbs', {url: `/class/${classValue}/land`})
		.then((resp) => {
			console.log('breadcrumbs: ', resp, resp.breadcrumbs)
			crumbs = resp.breadcrumbs
		})
		return {crumbs, classValue}
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
