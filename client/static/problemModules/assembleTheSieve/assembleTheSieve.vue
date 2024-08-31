<template>
    <div class="game_plot">
        <div class="answer_area" ref="answerArea">
            <div class="header"> Код: </div>
            <img v-for="codeBlock in answerAreaBlocks" @mousedown="moveFromAnswerArea(codeBlock.num, $event)" 
                @touchstart="moveFromAnswerArea(codeBlock.num, $event.touches[0])" :class="[codeBlock.type, 'block']"
                :src="`/problem_assets/assemble_the_sieve/block_${codeBlock.num}.svg`"/>
        </div>
        <div class="start_area">
            <img v-for="codeBlock in startAreaBlocks" @mousedown="moveFromStartArea(codeBlock.num, $event)" 
                @touchstart="moveFromStartArea(codeBlock.num, $event.touches[0])" :class="[codeBlock.type, 'block']"
                ref="startArea"
                :src="`/problem_assets/assemble_the_sieve/block_${codeBlock.num}.svg`"/>
        </div>
        <img :class="['block', 'target_block', targetBlock.type]" v-if="targetBlock" :style="`left: ${targetBlock.x}px; top: ${targetBlock.y}px`" 
            :src="`/problem_assets/assemble_the_sieve/block_${targetBlock.num}.svg`"/>
    </div>
</template>

<script>
export default {
    props: ['problemParams'],

    model: {
        prop: 'answer',
        event: 'updateAnswer',
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
                if (block.type != 'select') {
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
            let newStartAreaBlocks = []
            for (let block of this.startAreaBlocks) {
                if (block.num != blockNum) {
                    newStartAreaBlocks.push(block)
                }
            }
            this.startAreaBlocks = newStartAreaBlocks
            this.startDrag(event)
        },

        moveFromAnswerArea(blockNum, event) {
            event.preventDefault()
            this.targetBlock = {num: blockNum, type: 'usual'}
            let newAnswerAreaBlocks = []
            for (let block of this.answerAreaBlocks) {
                if (block.num != blockNum) {
                    newAnswerAreaBlocks.push(block)
                }
            }
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
            else {
                let newStartAreaBlocks = this.startAreaBlocks
                newStartAreaBlocks.push({num: this.targetBlock.num, type: 'usual'})
                this.startAreaBlocks = newStartAreaBlocks
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
