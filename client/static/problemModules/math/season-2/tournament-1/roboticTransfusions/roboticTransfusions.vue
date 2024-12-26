<template>
	<TransfusionLayout :vessel-config="config"/>
</template>

<script>
import TransfusionLayout from '~/static/problemModules/components/Transfusion/TransfusionLayout.vue';

export default {
	components: {
		TransfusionLayout,
	},
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	computed: {
		config() {
			console.log(this.problemParams.start_config)
			return this.problemParams.start_config;
		}
	}
}
</script>