<template>
	<div class="game_plot">
		<div  ref="answerArea" class="answer_area">
			<div class="header"> Код: </div>
			<img 
				v-for="(codeBlock, num) in answerAreaBlocks" :key="`start_area_block_${num}`" 
				:class="[codeBlock.type, 'block']"
				 :src="`/problem_assets/assemble_the_sieve/block_${codeBlock.num}.svg`"
				@mousedown="moveFromAnswerArea(codeBlock.num, $event)" 
				@touchstart="moveFromAnswerArea(codeBlock.num, $event.touches[0])"/>
		</div>
		<div class="start_area">
			<img 
				v-for="(codeBlock, num) in startAreaBlocks" :key="`answer_area_block_${num}`" 
				ref="startArea"
				:class="[codeBlock.type, 'block']"
				:src="`/problem_assets/assemble_the_sieve/block_${codeBlock.num}.svg`"
				@mousedown="moveFromStartArea(codeBlock.num, $event)" 
				@touchstart="moveFromStartArea(codeBlock.num, $event.touches[0])" />
		</div>
		<img 
			v-if="targetBlock" :class="['block', 'target_block', targetBlock.type]" 
			:style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px`" 
			:src="`/problem_assets/assemble_the_sieve/block_${targetBlock.num}.svg`"/>
	</div>
</template>

<script>
export default {

	model: {
		prop: 'answer',
		event: 'updateAnswer',
	},

	props: {
		problemParams: {
			type: Object,
			default: () => { return {} }
		}
	},


	data() {
		return {
			startAreaBlocks: [
								{num: 0, type: 'usual'},
								{num: 1, type: 'usual'}, 
								{num: 2, type: 'usual'}, 
								{num: 3, type: 'usual'}, 
								{num: 4, type: 'usual'}, 
								{num: 5, type:'usual'}, 
								{num: 6, type: 'usual'}
							],
			answerAreaBlocks: [],
			nearestPlaceToInsert: undefined,
			targetBlock: undefined,
			dragMode: false,
		}
	},

	mounted() {
		document.addEventListener('mousemove', this.drag, {passive: false})
		document.addEventListener('touchmove', this.drag, {passive: false})
		document.addEventListener('touchend', this.endDrag)
		document.addEventListener('mouseup', this.endDrag)
	},

	methods: {
		autoscroll() {
			const targetX = window.event.clientX
			const targetY = window.event.clientY
			const xDiff = 100
			const yDiff = 100
			let [scrollX, scrollY] = [0, 0]
			if (targetX + xDiff > window.innerWidth) {
				scrollX = targetX + xDiff - window.innerWidth
			}
			else if (targetX - xDiff < 0) {
				scrollX = targetX - xDiff
			}
			if (targetY + yDiff > window.innerHeight) {
				scrollY = targetY + yDiff - window.innerHeight
			}
			else if (targetY - yDiff < 0) {
				scrollY = targetY - yDiff
			}
			scrollBy(scrollX, scrollY)
		},

		inAllowedArea() { // if target object in allowed aarea
			const targetX = window.event.clientX
			const targetY = window.event.clientY
			if (targetX < 0 || targetX > window.innerWidth)
				return false
			if (targetY < 0 || targetY > window.innerHeight)
				return false
			return true
		},

		inRect(x, y, rect){
			if (x > rect.right || x < rect.left) {
				return false
			}
			if (y > rect.bottom || y < rect.top) {
				return false
			}
			return true
		},

		findNewNearestPlaceToInsert(y) {
			let index = 0
			const blocks = document.querySelectorAll('.answer_area .block')
			for (const block of blocks) {
				const blockRect = block.getBoundingClientRect()
				if (y >= (blockRect.top + blockRect.bottom) / 2 && !block.classList.contains('select')){
					index += 1
				}
			}
			return index
		},

		removeSelectedBlock() {
			const answerAreaBlocksProto = JSON.parse(JSON.stringify(this.answerAreaBlocks))
			const newAnswerAreaBlocks = []
			for (const block of answerAreaBlocksProto) {
				if (block.type !== 'select') {
					newAnswerAreaBlocks.push(block)
				}
			}
			this.answerAreaBlocks = newAnswerAreaBlocks
			this.$emit('updateAnswer', this.answerAreaBlocks)
		},

		updateNearestPlaceToInsert(x, y) {
			if (!this.inRect(x, y, this.$refs.answerArea.getBoundingClientRect())) {
				this.removeSelectedBlock()
				this.nearestPlaceToInsert = undefined
				return;
			}
			this.removeSelectedBlock()
			const newIndex = this.findNewNearestPlaceToInsert(y)
			this.nearestPlaceToInsert = newIndex
			const newAnswerAreaBlocks = JSON.parse(JSON.stringify(this.answerAreaBlocks))
			if (newIndex >= newAnswerAreaBlocks.length) {
				newAnswerAreaBlocks.push({num: this.targetBlock.num, type: 'select'})
			}
			else {
				newAnswerAreaBlocks.splice(newIndex, 0, {num: this.targetBlock.num, type: 'select'})
			}
			this.answerAreaBlocks = newAnswerAreaBlocks
			this.$emit('updateAnswer', this.answerAreaBlocks)
		},

		moveAt(x, y) {
			this.autoscroll()
			this.$set(this.targetBlock, 'x', x)
			this.$set(this.targetBlock, 'y', y)
			if (!this.inAllowedArea()) {
				this.endDrag()
			}
		},

		moveFromStartArea(blockNum, event) {
			event.preventDefault()
			this.targetBlock = {num: blockNum, type: 'usual'}
			const newStartAreaBlocks = []
			for (const block of this.startAreaBlocks) {
				if (block.num !== blockNum) {
					newStartAreaBlocks.push(block)
				}
			}
			this.startAreaBlocks = newStartAreaBlocks
			this.startDrag(event)
		},

		moveFromAnswerArea(blockNum, event) {
			event.preventDefault()
			this.targetBlock = {num: blockNum, type: 'usual'}
			const newAnswerAreaBlocks = []
			for (const block of this.answerAreaBlocks) {
				if (block.num !== blockNum) {
					newAnswerAreaBlocks.push(block)
				}
			}
			this.answerAreaBlocks = newAnswerAreaBlocks
			this.$emit('updateAnswer', this.answerAreaBlocks)
			this.startDrag(event)
		},

		startDrag(event) {
			const x = event.clientX
			const y = event.clientY
			this.dragMode = true
			this.moveAt(x, y)
		},

		drag(event) {
			if (!this.dragMode) {
				return
			}
			if (this.targetBlock === undefined)
				return
			let x, y
			if (event.touches) {
				event.preventDefault()
				x = event.touches[0].clientX
				y = event.touches[0].clientY
			}
			else {
				x = event.clientX
				y = event.clientY
			}
			this.moveAt(x, y)
			this.updateNearestPlaceToInsert(x, y)
		},

		endDrag() {
			if (!this.dragMode) {
				return
			}
			if (this.nearestPlaceToInsert !== undefined) {
				this.$set(this.answerAreaBlocks, this.nearestPlaceToInsert, this.targetBlock)
				this.$emit('updateAnswer', this.answerAreaBlocks)
			}
			else {
				const newStartAreaBlocks = this.startAreaBlocks
				newStartAreaBlocks.push({num: this.targetBlock.num, type: 'usual'})
				this.startAreaBlocks = newStartAreaBlocks
			}
			this.dragMode = false
			this.targetBlock = undefined
			this.nearestPlaceToInsert = undefined
		}
	},

}
</script>
