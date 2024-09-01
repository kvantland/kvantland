<template>
	<div class="game_plot">
		<div class="first_row">
			<div class="maze_border">
				<svg class="maze" version="1.1" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
				preserveAspectRatio="xMidYMid meet" 
				overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
					<g v-for="(row, rowNum) in maze" :transform="`translate(0 ${rowNum * mazeSide})`">
						<g v-if="rowNum > 0" v-for="(column, columnNum) in verticalWalls(row)">
							<line :class="column ? 'border' : 'usual'" :x1="columnNum * mazeSide" y1="0" :x2="columnNum * mazeSide" :y2="-mazeSide" />
						</g>
						<g v-for="(column, columnNum) in horizontalWalls(row)">
							<line :class="column ? 'border' : 'usual'" :x1="columnNum * mazeSide" y1="0" :x2="(columnNum + 1) * mazeSide" y2="0" />
						</g>
					</g>
				</svg>
			</div>
			<div class="start_area">
				<p>C помощью команд и цикловой конструкции:</p>
				<div v-for="block in commands" :class="['block', block.type]" @mousedown="moveFromStartArea(block, $event)" 
                @touchstart="moveFromStartArea(block, $event.touches[0])">
					<p>{{ block.text }}</p>
					<div v-if="block.type === 'cycle'" class="insert_zone"></div>
				</div>
			</div>
		</div>
		<div class="description">
			<p><b>Соберите код, который поможет роботу дойти из клетки S в клетку F. </b></p>
			<p>Суммарно разрешено использовать не более 7 блоков (блоком считается и цикловая конструкция, и команда). 
			Также роботу следует выполнить не более 100 поворотов или шагов вперед.</p>
		</div>
		<div class="second_row answer_area" ref="answerArea">
			<p style="font-size: 30px; font-weight: 700;"> Код: </p>
			<div class="block_with_num" v-for="(block, blockNum) in answerAreaBlocks">
				<div class="block_num"> {{ blockNum + 1 }}. </div>
				<div :class="['block', block.type]"  @mousedown="moveFromAnswerArea(blockNum, $event)" 
                @touchstart="moveFromAnswerArea(blockNum, $event.touches[0])"> 
					<p>{{ block.text }} </p>
						<div v-if="block.type === 'cycle'" class="insert_zone"></div>
				</div>
			</div>
		</div>
		<div v-if="targetBlock" :class="['block', targetBlock.type, 'target_block']" 
		:style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px	;`"> {{ targetBlock.text }} </div>
	</div>
</template>

<script>
export default {
	props: ['problemParams'],

	data() {
		return {
			mazeSide: 30,
			answerAreaBlocks: [],
			dragMode: false,
			nearestPlaceToInsert: undefined,
			targetBlock: undefined,
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

	methods: {
		verticalWalls(row) {
			let walls = []
			for (let symb of row.toString()) {
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
			let walls = []
			for (let symb of row.toString()) {
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
            //console.log(targetX, targetY)
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
            console.log(blocks)
            for (let block of blocks) {
                console.log(block.getBoundingClientRect())
                let blockRect = block.getBoundingClientRect()
                if (y >= (blockRect.top + blockRect.bottom) / 2 && !block.classList.contains('select')){
                    index += 1
                }
            }
            return index
        },

        removeSelectedBlock() {
            let answerAreaBlocksProto = JSON.parse(JSON.stringify(this.answerAreaBlocks))
            let newAnswerAreaBlocks = []
            for (let block of answerAreaBlocksProto) {
                if (block.type.split(' ')[0] != 'select') {
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
            let newIndex = this.findNewNearestPlaceToInsert(y)
            console.log('index to insert: ', newIndex)
            this.nearestPlaceToInsert = newIndex
            let newAnswerAreaBlocks = JSON.parse(JSON.stringify(this.answerAreaBlocks))
            if (newIndex >= newAnswerAreaBlocks.length) {
                newAnswerAreaBlocks.push({text: this.targetBlock.text, type: `select ${this.targetBlock.type}`})
            }
            else {
                newAnswerAreaBlocks.splice(newIndex, 0, {text: this.targetBlock.text, type: `select ${this.targetBlock.type}`})
            }
            this.answerAreaBlocks = newAnswerAreaBlocks
            this.$emit('updateAnswer', this.answerAreaBlocks)
        },

        moveAt(x, y) {
            this.autoscroll()
            this.$set(this.targetBlock, 'x', x)
            this.$set(this.targetBlock, 'y', y)
			console.log(this.targetBlock.x, this.targetBlock.y)
            if (!this.inAllowedArea()) {
                this.endDrag()
            }
        },

        moveFromStartArea(block, event) {
            this.targetBlock = block
            this.startDrag(event)
        },

        moveFromAnswerArea(blockNum, event) {
            this.targetBlock = this.answerAreaBlocks[blockNum]
            let newAnswerAreaBlocks = this.answerAreaBlocks
            newAnswerAreaBlocks.splice(blockNum, 1)
            this.answerAreaBlocks = newAnswerAreaBlocks
            this.$emit('updateAnswer', this.answerAreaBlocks)
            this.startDrag(event)
        },

        startDrag(event) {
            let x, y
            x = event.clientX
            y = event.clientY
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
                console.log('end move', this.targetBlock, this.nearestPlaceToInsert)
                this.$set(this.answerAreaBlocks, this.nearestPlaceToInsert, this.targetBlock)
                this.$emit('updateAnswer', this.answerAreaBlocks)
            }
            this.dragMode = false
            this.targetBlock = undefined
            this.nearestPlaceToInsert = undefined
        }
	},

	mounted() {
        document.addEventListener('mousemove', this.drag, {passive: false})
        document.addEventListener('touchmove', this.drag, {passive: false})
        document.addEventListener('touchend', this.endDrag)
        document.addEventListener('mouseup', this.endDrag)
    }
}
</script>