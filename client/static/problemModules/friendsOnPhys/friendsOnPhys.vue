<template>
    <svg version="1.1" ref="svg" class="display_svg" :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
        preserveAspectRatio="xMidYMid meet" 
        overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g class="answer_container" ref="ans_container">
            <image class="answer_container" x="0" y="0" :width="answerAreaWidth" :height="answerAreaHeight" href="/problem_assets/friend_on_phys/field.png" />
            <g class="answer_position" v-for="(boy, boyNum) in boysAmount" :transform="`translate(${(boyGap + boyHeight) * boyNum + fieldGap} ${answerAreaHeight / 2} )`">
                <rect :class="['answer_rect', `rect_${boyNum}`, nearestRectNum == boyNum && !answerAreaBoys[nearestRectNum] ? 'active' : 'notActive']" :x="-boardWidth / 2" :y="-(boyHeight) / 2" :width="boyWidth" :height="boyHeight + boardHeight" />
                <g class="boy" v-if="answerAreaBoys[boyNum]" @mousedown="moveFromAnsArea(answerAreaBoys[boyNum])" @touchstart="moveFromAnsArea(answerAreaBoys[boyNum])"
                    v-html="answerAreaBoys[boyNum].html" />
            </g>
        </g>
        <g class="drag_container" :transform="`translate(${answerAreaWidth} 0)`">
            <g class="rows" :transform="`translate(0 ${boyGap})`">
                <g v-for="(row, rowNum) in rows" class="row" :transform="`translate(${boyGap} ${(boyGap + boyWidth) * rowNum})`">
                    <g v-for="(boy, boyNum) in inRow" v-if="startAreaBoys[boyNum + rowNum * inRow]" 
                        :transform="`translate(${boyCoordinates[boyNum + rowNum * inRow].x} ${boyCoordinates[boyNum + rowNum * inRow].y})`"
                        @touchstart="moveFromStartArea(boyNum + rowNum * inRow, $event.touches[0])" 
                        @mousedown="moveFromStartArea(boyNum + rowNum * inRow, $event)"
                        :class="`boy boy_${boyNum + rowNum * inRow}`">
                            <image x="0" y="0" :height="boyHeight" :width="boyWidth" :href="`/problem_assets/friend_on_phys/boy${boyNum + rowNum * inRow + 1}.png`" />
                            <g class="board" :transform="`translate(0 ${boyHeight})`">
                                <image class="board" x="0" y="0" :width="boardWidth" :height="boardHeight" href="/problem_assets/board.svg" />
                                <text class="boardName" :x="boardWidth / 2" :y="boardHeight / 2" dy="0.35em"> {{ boardNames[boyNum + rowNum * inRow] }} </text>
                            </g>
                    </g>
                </g>
            </g>
        </g>
        <g v-if="dragMode" class="choiced" :transform="`translate(${targetBoy.x} ${targetBoy.y})`" ref="choiced">           
            <image :x="-boyWidth / 2" :y="-boyHeight / 2" :height="boyHeight" :width="boyWidth" :href="`/problem_assets/friend_on_phys/boy${targetBoy.index+1}.png`" />
            <g class="board" :transform="`translate(${-boyWidth / 2} ${boyHeight / 2})`">
                <image class="board" x="0" y="0" :width="boardWidth" :height="boardHeight" href="/problem_assets/board.svg" />
                <text class="boardName" :x="boardWidth / 2" :y="boardHeight / 2" dy="0.35em"> {{ boardNames[targetBoy.index] }} </text>
            </g>
        </g>
    </svg>
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
            boyCoordinates: [], 
            boardNames: ['Алёша', 'Боря', 'Вася', 'Гриша'],
            boardHeight: 30,
            inRow: 2,
            rows: 2,
            boyGap: 15,
            boyHeight: 140,
            boyWidth: 140,
            dropAllowDistance: 70,
            targetBoy: {x: 0, y:0, index: undefined},
            nearestRectNum: undefined,
            allowedDistToDrop: 100,

            startAreaBoys: {},   
            answerAreaBoys: [],
            dragMode: false, //is drag?
        }
    },
    computed: {
        boardWidth() {
            return this.boyWidth
        },
        dragAreaWidth() {
            return this.inRow * (this.boyWidth + this.boyGap) + this.boyGap
        },
        dragAreaHeight() {
            return this.rows * (this.boyHeight + this.boyGap + this.boardHeight) + this.boyGap
        },
        answerAreaWidth() {
            return this.boyGap * (this.boysAmount + 1) + this.boyWidth * this.boysAmount
        },
        answerAreaHeight(){
            return this.dragAreaHeight
        },
        fieldGap() {
            return (this.answerAreaWidth - (this.boyGap + this.boyWidth) * (this.boysAmount - 1)) / 2
        },
        svgHeight() {
            return this.dragAreaHeight
        },
        svgWidth() {
            return this.answerAreaWidth + this.dragAreaWidth
        },
        boysAmount() {
            return this.boardNames.length
        }
    },
    methods: {
        convertDOMtoSVG(x, y) {
            try {
                const pt = new DOMPoint(x, y)
	            const svgP = pt.matrixTransform(this.$refs['svg'].getScreenCTM().inverse())
                return {x: svgP.x, y: svgP.y}
            }
            catch(e) {
                return false
            }
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
        getNearestRectNum(x, y) {
            let minDist = 1000000000000
            let optimalNum = null
            for(let rectNum = 0; rectNum < this.boysAmount; rectNum++) {
                let rect = document.querySelector(`.rect_${rectNum}`).getBoundingClientRect()
                let rectCenterCoordinates = {
                    x: rect.width / 2 + rect.left,
                    y: rect.height / 2 + rect.top
                }
                let dist = Math.hypot(x - rectCenterCoordinates.x, y - rectCenterCoordinates.y)
                if (dist < minDist) {
                    minDist = dist
                    optimalNum = rectNum
                }
            }
            if (minDist <= this.allowedDistToDrop)
                return optimalNum
            return null
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
        
        inRect(x, y, rect){
            if (x > rect.right || x < rect.left) {
                return false
            }
            if (y > rect.bottom || y < rect.top) {
                return false
            }
            return true
        },
        moveAt(x, y) {
            const newCursorCoordinates = this.convertDOMtoSVG(x, y)
            if (!newCursorCoordinates)
                return
            this.autoscroll()
            this.$set(this.targetBoy, 'x', newCursorCoordinates.x)
            this.$set(this.targetBoy, 'y', newCursorCoordinates.y)
            if (!this.inAllowedArea()) {
                this.endDrag()
            }
        },
        startDrag(index, event) {
            let x, y
            console.log(index)
            if (event.touches) {
                x = event.touches[0].clientX
                y = event.touches[0].clientY
            }
            else {
                x = event.clientX
                y = event.clientY
            }
            this.dragMode = true
            this.$set(this.targetBoy, 'index', index)
            this.moveAt(x, y)
        },
        drag(event) {
            if (!this.dragMode) {
                return
            }
            if (this.targetBoy.index == undefined)
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
            this.nearestRectNum = this.getNearestRectNum(x, y)
            this.moveAt(x, y)
        },
        endDrag() {
            if (!this.dragMode) {
                return
            }
            if (this.nearestRectNum === undefined) {
                this.backToStartArea()
            }
            else {
                if (this.answerAreaBoys[this.nearestRectNum]) 
                    this.backToStartArea()
                else
                    this.dropToAnsArea()
            }
            this.dragMode = false
            this.nearestRectNum = undefined
        },
        dropToAnsArea() {
            const newAnswerAreaBoy = {
                index: this.targetBoy.index,
                html: this.$refs.choiced.innerHTML
            }
            console.log(newAnswerAreaBoy)
            this.$set(this.answerAreaBoys, this.nearestRectNum, newAnswerAreaBoy)

            let newAnswerAreaBoysIndex = []
            for (const boy of this.answerAreaBoys) {
                if (!boy) {
                    newAnswerAreaBoysIndex.push(-1)
                    continue;
                }
                newAnswerAreaBoysIndex.push(boy.index + 1)
            }
            this.$emit('updateAnswer', newAnswerAreaBoysIndex)
            console.log('ans', newAnswerAreaBoysIndex)
        },
        backToStartArea() {
            const dragIndex = this.targetBoy.index
            this.startAreaBoys[dragIndex] = true
        },
        moveFromStartArea(index, event) {
            this.$set(this.startAreaBoys, index, false)
            this.startDrag(index, event)
        },
        moveFromAnsArea(boy) {
            console.log(boy)
            let newAnswerAreaBoys = []
            for (let boyNum = 0; boyNum < this.boysAmount; boyNum++) {
                if (!this.answerAreaBoys[boyNum]) {
                    continue;
                }
                if (this.answerAreaBoys[boyNum].index == boy.index) {
                    this.$set(this.answerAreaBoys, boyNum, undefined)
                }   
            }
            let newAnswerAreaBoysIndex = []
            for (const boy of newAnswerAreaBoys) {
                newAnswerAreaBoysIndex.push(boy.index + 1)
            }
            this.$emit('updateAnswer', newAnswerAreaBoysIndex)
            this.startDrag(boy.index, window.event)
        }
    },
    created() {
        let coordinates = []
        let startBoys = {}
        for (let row = 1; row <= this.rows; row++) {
            for (let column = 1; column <= this.inRow; column++) {
                coordinates.push({x: (column - 1) * (this.boyGap + this.boyWidth), y: this.boardHeight * (row - 1)})
                startBoys[(column - 1) + this.inRow * (row - 1)] = true
            }
        }
        this.boyCoordinates = coordinates
        this.startAreaBoys = startBoys
    },
    mounted() {
        document.addEventListener('mousemove', this.drag, {passive: false})
        document.addEventListener('touchmove', this.drag, {passive: false})
        document.addEventListener('touchend', this.endDrag)
        document.addEventListener('mouseup', this.endDrag)
    }
}
</script>
