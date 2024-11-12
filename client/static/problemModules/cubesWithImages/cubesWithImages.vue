<template>
	<div class="cubes-container">
		<div 
			v-for="cube, cubeNum in cubes" :key="`cube_num-${cubeNum}`"
			class="cube-with-num">
			<img 
				:class="['cube-with-num__cube', choosed === cubeNum ? 'cube-with-num__cube_active' : 'cube-with-num__cube_passive']" 
				:src="`/problem_assets/cubes_with_images/cube_${cube}.svg`"
				@click="choose(cube, cubeNum)" />
			<p class="cube-with-num__num"> {{ alph[cubeNum] }} </p>
		</div>
	</div>
</template>


<script>
export default {
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
		return {
			alph: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
			choosed: undefined
		}
	},
	computed: {
		cubes() {
			return this.problemParams.cubeList
		}
	},
	methods: {
		choose(cube, index) {
			console.log('choosed: ', cube)
			this.choosed = index
			this.$emit('updateAnswer', cube)
		}
	}
}
</script>