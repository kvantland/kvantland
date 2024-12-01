<template>
	<ChooseTable
		v-if="config.length"
		:plot-config="config"
		:choosed-color="'rgba(0, 255, 0, 0.2)'"
		@updateAnswer="updateAnswer"
		@updateConfig="updateConfig" />
</template>

<script>
import ChooseTable from '~/static/problemModules/components/ChooseTable.vue';

export default {
	components: {
		ChooseTable,
	},
	model: {
		prop: 'answer',
		event: 'updateAnswer'
	},
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	data() {
		const startConfig = this.problemParams?.orchard_config
		const config = []

		for (let rowNum = 0; rowNum < startConfig.length; rowNum++) {
			config.push([])
			for (let columnNum = 0; columnNum < startConfig[0].length; columnNum++) {
				const hasTree = startConfig[rowNum][columnNum]
				config[rowNum].push({active: true, choosed: false, image: undefined})
				if (hasTree) {
					config[rowNum][columnNum].image = 'apple_orchard/tree.svg'
				}
			}
		}
		console.log(config)
		return {
			config
		}
	},
	methods: {
		updateConfig(config) {
			this.config = config
		},
		updateAnswer(answer) {
			console.log(answer)
			this.$emit('updateAnswer', answer)
		}
	}
}
</script>