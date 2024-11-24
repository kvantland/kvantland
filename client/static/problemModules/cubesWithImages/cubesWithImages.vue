<template>
	<div class="cubes-container">
		<div 
			v-for="cube, cubeNum in cubes" :key="`cube_num-${cubeNum}`"
			:class="['cube-with-num', choosed === cubeNum ? 'cube-with-num_active' : 'cube-with-num_passive']"
			@click="choose(cube, cubeNum)" >
			<img 
				:class="['cube-with-num__cube']" 
				:src="`/problem_assets/cubes_with_images/cube_${cube}.svg`"
				/>
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