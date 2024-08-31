<template>
    <div class="game_plot">
        <div class="start_area">
            <div class="main_blocks block_line">
                <div v-for="(blockText, blockNum) in mainBlocks" class="block main_block" :key="`main_block_${blockNum}`"
                @touchstart="moveFromStartArea(text=blockText, type='main_block', $event.touches[0])" 
                @mousedown="moveFromStartArea(text=blockText, type='main_block', $event)"> {{ blockText }} </div>
            </div>
            <div class="other_blocks block_line">
                <div v-for="(blockText, blockNum) in logicalBlocks" class="block logical_block" :key="`logical_block_${blockNum}`"
                @touchstart="moveFromStartArea(text=blockText, type='logical_block', $event.touches[0])" 
                @mousedown="moveFromStartArea(text=blockText, type='logical_block', $event)"> {{ blockText }} </div>
                <div v-for="(blockText, blockNum) in syntaxBlocks" class="block syntax_block" :key="`syntax_block_${blockNum}`"
                @touchstart="moveFromStartArea(text=blockText, type='syntax_block', $event.touches[0])" 
                @mousedown="moveFromStartArea(text=blockText, type='syntax_block', $event)"> {{ blockText }} </div>
            </div>
        </div>
        <div class="answer_area_with_sign">
            <p class="answer_sign"> Ответ </p>
            <div class="answer_area" ref="answerArea">
                <div v-for="(block, blockNum) in expression" :key="`expression_block_${blockNum}`" :class="['block', block.type]"
                @touchstart="moveFromAnswerArea(blockNum, $event.touches[0])"
                @mousedown="moveFromAnswerArea(blockNum, $event)"> {{ block.text }} </div>
            </div>
        </div>
        <div class="target_block" v-if="targetBlock" :class="['block', targetBlock.type]" 
        :style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px`"> {{ targetBlock.text }} </div>
    </div>
</template>

<script>
export default {
    props: ['problemParams'],

    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },

    data() {
        return {
            logicalBlocks: ['И', 'ИЛИ', 'НЕ', 'XOR'],
            syntaxBlocks: ['(', ')'],
            targetBlock: undefined,
            dragMode: false,
            nearestPlaceToInsert: undefined,
            expression: [],
        }
    },

    computed: {
        mainBlocks() {
            return this.problemParams.blocks
        },
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
            console.log(targetX, targetY)
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

        findNewNearestPlaceToInsert(x) {
            let index = 0
            const blocks = document.querySelectorAll('.answer_area .block')
            console.log(blocks)
            for (let block of blocks) {
                console.log(block.getBoundingClientRect())
                let blockRect = block.getBoundingClientRect()
                if (x >= (blockRect.left + blockRect.right) / 2 && !block.classList.contains('select_block')){
                    index += 1
                }
            }
            return index
        },

        removeSelectedBlock() {
            let newExpressionProto = JSON.parse(JSON.stringify(this.expression))
            let newExpression = []
            for (let block of newExpressionProto) {
                if (block.type != 'select_block') {
                    newExpression.push(block)
                }
            }
            this.expression = newExpression
            this.$emit('updateAnswer', this.expression)
        },

        updateNearestPlaceToInsert(x, y) {
            if (!this.inRect(x, y, this.$refs.answerArea.getBoundingClientRect())) {
                this.removeSelectedBlock()
                this.nearestPlaceToInsert = undefined
                return;
            }
            this.removeSelectedBlock()
            console.log('expression: ', this.expression)
            let newIndex = this.findNewNearestPlaceToInsert(x)
            console.log('index to insert: ', newIndex)
            this.nearestPlaceToInsert = newIndex
            let newExpression = JSON.parse(JSON.stringify(this.expression))
            if (newIndex >= this.expression.length) {
                newExpression.push({text: this.targetBlock.text, type: 'select_block'})
            }
            else {
                newExpression.splice(newIndex, 0, {text: this.targetBlock.text, type: 'select_block'})
            }
            this.expression = newExpression
            this.$emit('updateAnswer', this.expression)
        },

        moveAt(x, y) {
            this.autoscroll()
            this.$set(this.targetBlock, 'x', x)
            this.$set(this.targetBlock, 'y', y)
            if (!this.inAllowedArea()) {
                this.endDrag()
            }
        },

        moveFromStartArea(text, type, event) {
            this.targetBlock = {text: text, type: type}
            this.startDrag(event)
        },

        moveFromAnswerArea(num, event) {
            this.targetBlock = this.expression[num]
            let newExpression = JSON.parse(JSON.stringify(this.expression))
            newExpression.splice(num, 1)
            this.expression = newExpression
            this.$emit('updateAnswer', this.expression)
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
                this.$set(this.expression, this.nearestPlaceToInsert, this.targetBlock)
                this.$emit('updateAnswer', this.expression)
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