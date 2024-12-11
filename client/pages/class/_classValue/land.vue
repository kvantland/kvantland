<template>
	<div>
		<div class="content_wrapper_land">
			<Breadcrumbs :crumbs="crumbs" />
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

	async asyncData({params, $axios}) {
		console.log(params.classValue)
		let crumbs
		await $axios.$post('/api/breadcrumbs', {url: `/class/${params.classValue}/land`})
		.then((resp) => {
			console.log('breadcrumbs: ', resp, resp.breadcrumbs)
			crumbs = resp.breadcrumbs
		})
		return {crumbs,}
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
