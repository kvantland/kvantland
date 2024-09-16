<template>
	<div class="examples_with_header">
		<p class="header"> Примеры: </p>
		<div class="examples">
			<div class="block title" >
				<p>Стандартный ввод</p>
			</div>
			<div class="block title">
				<p>Стандартный вывод</p>
			</div>
			<template
				v-for="(lines, num) in inputExamples">
				<div :key="`input_${num}`" class="block input" >
					<p 
						v-for="(line, lineNum) in lines.input" :key="`input_example_${num}_line_${lineNum}`">
						{{ line }}
					</p>
				</div>
				<div :key="`output_${num}`" class="block output" >
					<p 
						v-for="(line, lineNum) in lines.output" :key="`output_example_${num}_line_${lineNum}`">
						{{ line }}
					</p>
				</div>
			</template>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		inputExamples: {
			type: Array,
			default: () => {return []},
		}
	}
}
</script>

<style scoped>
.examples_with_header {
	display: flex;
	flex-direction: column;
	margin: 30px 0;
}

.header {
	font-weight: 700;
}

.examples {
	display: inline-grid;
	grid-template-columns: 1fr 1fr;
	grid-template-rows: auto;
	align-items: start;
	width: 100%;
	background-color:  #6B6B6B80;
	gap: 4px;
}

.block {
	align-self: stretch;
	display: flex;
	flex-direction: column;
	background-color: white;
	justify-content: center;
	padding: 10px 0;
	padding-left: 10%;
	margin-bottom: -2px;
}

.block.title {
	align-items: center;
	justify-content: center;
	margin-bottom: 0px;
}
</style>