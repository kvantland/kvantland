<template>
	<div class="game_plot">
		<div class="first_row">
			<div class="maze_border">
				<svg class="maze" version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
				preserveAspectRatio="xMidYMid meet" 
				overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
					<g v-for="(row, rowNum) in maze" :key="`row_${rowNum}`" :transform="`translate(0 ${rowNum * mazeSide})`" >
						<g v-if="rowNum > 0">
							<line  v-for="(column, columnNum) in verticalWalls(row)"  :key="`vertical_line_${columnNum}`" 
								:class="column ? 'border' : 'usual'" :x1="columnNum * mazeSide" y1="0" :x2="columnNum * mazeSide" :y2="-mazeSide" />
						</g>
						<g v-for="(column, columnNum) in horizontalWalls(row)" :key="`horizontal_line_${columnNum}`">
							<line :class="column ? 'border' : 'usual'" :x1="columnNum * mazeSide" y1="0" :x2="(columnNum + 1) * mazeSide" y2="0" />
						</g>
					</g>
				</svg>
			</div>
			<div class="start_area">
				<p>C помощью команд и цикловой конструкции:</p>
				<div v-for="(block, blockNum) in commands" :key="`start_area_block_${blockNum}`" :class="['block', block.type]" 
					@mousedown="moveFromStartArea(block, $event)" 
					@touchstart="moveFromStartArea(block, $event.touches[0])">
					<p>{{ block.text }}</p>
					<div v-if="block.type === 'cycle'" class="insert_zone"></div>
				</div>
			</div>
		</div>
		<div class="description">
			<p><b>Соберите код, который поможет роботу дойти из клетки S в клетку F.</b></p>
			<p>Суммарно разрешено использовать не более 7 блоков (блоком считается и цикловая конструкция, и команда). 
			Также роботу следует выполнить не более 100 поворотов или шагов вперед.</p>
		</div>
		<div ref="answerArea" class="second_row answer_area">
			<p style="font-size: 30px; font-weight: 700;"> Код: </p>
			<div v-for="(block, blockNum) in answerAreaBlocks" :key="`block_with_num_${blockNum}`" class="block_with_num">
				<div class="block_num"> {{ blockNum + 1 }}. </div>
				<answerBlock :blockData="block" :answerAreaBlocks="answerAreaBlocks" :targetBlock="targetBlock"
					@updateAnswerArea="updateAnswerArea" @updateTargetBlock="updateTargetBlock" @startDrag="startDrag($event)"></answerBlock>
			</div>
		</div>
		<div v-if="targetBlock" :class="['block', targetBlock.type, 'target_block']" 
			:style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px	;`"> {{ targetBlock.text }} </div>
	</div>
</template>

<script>
import answerBlock from './components/answerBlock.vue';

export default {
	components: {answerBlock},

	props: {
		problemParams:{
			type: Object,
			default() {
				return {}
			},
		}
	},

	data() {
		return {
			mazeSide: 30,
			answerAreaBlocks: [],
			dragMode: false,
			nearestPlaceToInsert: undefined,
			targetBlock: undefined,
			currentBlockId: 1,
		}
	},

	computed: {
		maze() {
			return this.problemParams.maze
		},
		svgHeight() {
			return (this.maze.length - 1) * this.mazeSide
		},
		svgWidth() {
			return (this.maze.length - 1) * this.mazeSide
		},
		commands() {
			return this.problemParams.commands
		}
	},

	mounted() {
		document.addEventListener('mousemove', this.drag, {passive: false})
		document.addEventListener('touchmove', this.drag, {passive: false})
		document.addEventListener('touchend', this.endDrag)
		document.addEventListener('mouseup', this.endDrag)
	},

	methods: {
		verticalWalls(row) {
			const walls = []
			for (const symb of row.toString()) {
				if (symb === '.') {
					walls.push(false)
				}
				else if (symb === '|') {
					walls.push(true)
				}
			}
			return walls
		},

		horizontalWalls(row) {
			const walls = []
			for (const symb of row.toString()) {
				if (symb === ' ') {
					walls.push(false)
				}
				else if (symb === '_') {
					walls.push(true)
				}
			}
			return walls
		},

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
			// console.log(targetX, targetY)
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

		findNewNearestPlaceToInsert(y, level=document.querySelectorAll('.answer_area .block'), parent=this.currentBlockId) {
			let index = 0
			for (const block of level) {
				const blockRect = block.getBoundingClientRect()
				if (block.classList.contains('cycle') && !block.classList.contains('select')) {
					if (y >= blockRect.top && y <= blockRect.bottom) {
						const childLevel = document.querySelectorAll(`.answer_area .cycle.block[block_id='${block.getAttribute('block_id')}'] .block`)
						const newParent = block.getAttribute('block_id')
						const newIndex = this.findNewNearestPlaceToInsert(y, level=childLevel, parent=newParent)
						return newIndex
					}
				}
				if (y >= (blockRect.top + blockRect.bottom) / 2 && !block.classList.contains('select')) {
					index++
				}
			}
			return {index, parent}
		},

		removeSelectedBlock(level=this.answerAreaBlocks) {
			const newLevelBlocks = []
			for (const block of level) {
				const newBlock = JSON.parse(JSON.stringify(block))
				if (block.children) {
					newBlock.children = this.removeSelectedBlock(block.children)
				}
				if (!newBlock.select) {
					newLevelBlocks.push(newBlock)
				}
			}
			return newLevelBlocks
		},

		tryToInsertInto(index, parent, block) {
			const newBlock = JSON.parse(JSON.stringify(block))
			let newChildren = []
			if (block.id.toString() === parent.toString()) {
				if (block.children)	
					newChildren = JSON.parse(JSON.stringify(block.children))
				if (index < newChildren.length) {
					newChildren.splice(index, 0, this.targetBlock)
				}
				else {
					newChildren.push(this.targetBlock)
				}
			}
			else if (block.children) {
				for (const childBlock of block.children) {
					const newChildBlock = this.tryToInsertInto(index, parent, childBlock)
					newChildren.push(newChildBlock)
				}
			}
			newBlock.children = newChildren
			return newBlock
		},
		
		updateNearestPlaceToInsert(x, y) {
			this.answerAreaBlocks = this.removeSelectedBlock()
			const newIndex = this.findNewNearestPlaceToInsert(y)
			if (!this.inRect(x, y, this.$refs.answerArea.getBoundingClientRect()) || !(newIndex)) {
				this.nearestPlaceToInsert = undefined
				return;
			}

			const [index, parent] = [newIndex.index, newIndex.parent]
			console.log('index to insert: ', newIndex)
			this.nearestPlaceToInsert = newIndex
			this.targetBlock.select = true
			this.targetBlock.parent = parent
			const newAnswerAreaBlocks = []

			this.answerAreaBlocks.forEach(function(block, blockIndex) {
				if (parent.toString() !== this.currentBlockId.toString()) { // block has parent, different from itself
					const newBlock = this.tryToInsertInto(index, parent, block)
					newAnswerAreaBlocks.push(newBlock)
				}
				else {
					if (index.toString() === blockIndex.toString())
						newAnswerAreaBlocks.push(this.targetBlock)
					newAnswerAreaBlocks.push(block)
				}
			}.bind(this))

			if (index >= this.answerAreaBlocks.length && parent.toString() === this.currentBlockId.toString()) {
				newAnswerAreaBlocks.push(this.targetBlock)
			}
			this.answerAreaBlocks = newAnswerAreaBlocks
		},

		moveAt(x, y) {
			this.autoscroll()
			this.$set(this.targetBlock, 'x', x)
			this.$set(this.targetBlock, 'y', y)
			if (!this.inAllowedArea()) {
				this.endDrag()
			}
		},

		moveFromStartArea(block, event) {
			this.targetBlock = block
			this.targetBlock.id = this.currentBlockId
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
				this.targetBlock.select = false
				this.answerAreaBlocks = this.removeSelectedBlock()
				this.$emit('updateAnswer', this.answerAreaBlocks)
				this.currentBlockId += 1
			}
			this.dragMode = false
			this.targetBlock = undefined
			this.nearestPlaceToInsert = undefined
		},

		updateAnswerArea(newValue) {
			console.log('update Answer area', newValue)
			this.answerAreaBlocks = newValue
		},

		updateTargetBlock(newValue) {
			this.targetBlock = newValue
		},
	},
}
</script>