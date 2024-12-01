<template>
	<div class="game_plot">
		<p class="header">Код:</p>
		<div v-for="(block, blockNum) in codeBlocks" class="block_with_num">
			<div class="block_num">{{ blockNum + 1 }}</div>
			<div class="block">
				<div class="block_type">
					<p> {{ block.type }} </p>
					<img :class="['arrow', selectMode[blockNum] ? 'arrow_up' : 'arrow_down']" src="/problem_assets/arrow_down.svg" 
					@click="changeSelectMode(blockNum)"/>
				</div>
				<div class="select_list" v-if="selectMode[blockNum]">
					<div class="select_field" v-for="type in blockTypes" @click="changeType(blockNum, type)"> {{ type }} </div>
				</div>
				<div class="expression">
					<p>(</p>
					<div class="first_input input">
						<input maxlength="1" @keydown="isCorrectValue(blockNum, 'firstInputValue', $event)" :value="block.firstInputValue" 
						:input-save-value="block.firstInputValue">
					</div>
					<p>,</p>
					<div class="second_input input">
						<input maxlength="1" @keydown="isCorrectValue(blockNum, 'secondInputValue', $event)" :value="block.secondInputValue"
						:input-save-value="block.secondInputValue"/>
					</div>
					<p>)</p>
				</div>
			</div>
		</div>
		<img class="add" src="/problem_assets/add_symbol.svg" @click="addLine" />
	</div>
</template>

<script>
export default {
	props: ['problemParams'],

	model: {
		prop: 'answer',
		event: 'updateAnswer',
	},

	data(){
		return {
			codeBlocks: [],
			selectMode: [],
		}
	},

	computed: {
		blockTypes() {
			return this.problemParams.blockTypes
		},
		defaultBlockType() {
			return this.blockTypes[0]
		},
		maxLinesAmount() {
			return this.problemParams.max_lines_amount
		},
	},

	methods: {
		addLine() {
			if (this.codeBlocks.length >= this.maxLinesAmount) {
				this.$emit('showXhrDialog', "Программа должна состоять не более чем из 10 строк.")
				return
			}
			let newSelectMode = JSON.parse(JSON.stringify(this.selectMode))
			let newCodeBlocks = JSON.parse(JSON.stringify(this.codeBlocks))
			newCodeBlocks.push({type: this.defaultBlockType, firstInputValue:'', secondInputValue: ''})
			newSelectMode.push(false)
			this.selectMode = newSelectMode
			this.codeBlocks = newCodeBlocks
		},
		isCorrectValue(num, inputNum, event) {
			console.log(this.codeBlocks)
			const newValue = event.key
			if (newValue === 'Backspace') {
				console.log(newValue)
				this.$emit('updateAnswer', this.codeBlocks)
				return
			}
			if (inputNum === 'secondInputValue') {
				if (!['A', 'B', 'C', 'D'].includes(newValue.toUpperCase())) {	
					event.preventDefault()
					return 
				}
			}
			else if (inputNum === 'firstInputValue') {
				if (!['A', 'B', 'C', 'D', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].includes(newValue.toUpperCase())) {	
					event.preventDefault()
					return 
				}
			}
			console.log('update!')
			this.$set(this.codeBlocks[num], inputNum, newValue.toUpperCase()) 
			this.$emit('updateAnswer', this.codeBlocks)
		},

		changeSelectMode(blockNum) {
			let newSelectMode = []
			for (let modeNum = 0; modeNum < this.selectMode.length; modeNum++) {
				if (modeNum == blockNum) {
					newSelectMode.push(!this.selectMode[blockNum])
				}
				else {
					newSelectMode.push(false)
				}
			}
			this.selectMode = newSelectMode
		},

		changeType(blockNum, type) {
			console.log(type)
			let newCodeBlocks = JSON.parse(JSON.stringify(this.codeBlocks))
			let newSelectMode = JSON.parse(JSON.stringify(this.selectMode))
			newSelectMode[blockNum] = !newSelectMode[blockNum]
			newCodeBlocks[blockNum].type = type
			this.selectMode = newSelectMode
			this.codeBlocks = newCodeBlocks
			this.$emit('updateAnswer', this.codeBlocks)
		}
	}
}
</script>