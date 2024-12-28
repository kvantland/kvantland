<template>
	<TransfusionLayout 
		:vessel-config="config" 
		:max-height="maxHeight" 
		:new-xhr="newXhr"
		:xhr-data="xhrData"
		@xhrGet="$emit('xhrGet')"
		@showXhrDialog="(message) => {$emit('showXhrDialog', message)}"
		@transfusion="(data) => $emit('xhrRequest', data)"/>
</template>

<script>
import TransfusionLayout from '~/static/problemModules/components/Transfusion/TransfusionLayout.vue';

export default {
	components: {
		TransfusionLayout, 
	},
	props: {
		xhrData: {
      type: Object,
      default() {
        return {}
      },
    },
    newXhr: {
      type: Boolean,
      default: false,
    },
		problemParams: {
			type: Object,
			default: () => {}
		},
	},
	computed: {
		config() {
			return this.problemParams.current_config;
		},
		maxHeight() {
			return this.problemParams.max_height
		}
	},
}
</script>