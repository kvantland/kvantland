<template>
    <div class="svg_with_buttons">
    <svg version="1.1" ref="svg" class="display_svg" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" 
            :width="svgWidth" :height="svgHeight"
            overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <Scales @svgHeight="getSvgHeight" @svgWidth="getSvgWidth" @moveFromCup="moveFromCup" :scale="0.8" @stopMove="stopWeight"
            :leftCupObjects="cupWeights.left" :rightCupObjects="cupWeights.right" :moveTo="newSide" />
        <g class="containers" :transform="`translate(${(scalesWidth - containersAreaWidth) / 2} ${scalesHeight + dragAreaMarginTop})`">
            <g class="drag_container">
                <rect class="drag_container" :width="dragAreaWidth" :height="dragAreaHeight" x="0" y="0" fill="lightgrey" />
                <g class="rows" :transform="`translate(0 ${weightGap})`">
                    <g v-for="(row, rowNum) in rows" class="row" :transform="`translate(${weightGap} ${(weightGap + weightWidth) * rowNum})`">
                        <g v-for="(weight, weightNum) in inRow" v-if="startAreaWeights[weightNum + rowNum * inRow]" 
                            @touchstart="moveFromStartArea(weightNum + rowNum * inRow, $event.touches[0])" 
                            @mousedown="moveFromStartArea(weightNum + rowNum * inRow, $event)"
                            :transform="`translate(${weightCoordinates[weightNum + rowNum * inRow].x} ${weightCoordinates[weightNum + rowNum * inRow].y})`"
                            :class="`weight weight_${weightNum + rowNum * inRow}`">
                            <image x="0" y="0" :height="weightHeight" :width="weightWidth" href="/icons/weight.svg" />
                            <text class="name" :x="weightWidth / 2" :y="weightHeight / 2 + nameYPad"> {{ names[weightNum + rowNum * inRow] }} </text>
                        </g>
                    </g>
                </g>
            </g>
            <g class="answer_container" :transform="`translate(${containersGap + dragAreaWidth} 0)`" ref="ans_container">
                <rect class="answer_container" x="0" y="0" :width="answerAreaWidth" :height="answerAreaHeight" fill="lightgrey" />
                <g :transform="`translate(${weightWidth / 2 + weightGap} ${weightHeight / 2 + weightGap})`">
                    <g class="weight" v-for="(weight, weightNum) in answerAreaWeights" @mousedown="moveFromAnsArea(weight)" @touchstart="moveFromAnsArea(weight)"
                        :transform="`translate(0 ${(weightGap + weightHeight) * weightNum})`" v-html="weight.html" />
                </g>
            </g>
        </g>
        <g  v-if="dragMode" class="choiced" :transform="`translate(${targetWeight.x} ${targetWeight.y})`" ref="choiced">
            <image :x="-weightWidth / 2" :y="-weightHeight / 2" :height="weightHeight" :width="weightWidth" href="/icons/weight.svg" />
            <text class="name" x="0" :y="nameYPad"> {{ names[targetWeight.index] }} </text>
        </g>
    </svg>
    <div class="buttons">
        <button class="weight_button" @click="startWeight"> Взвесить </button>
        <button class="clear_button" @click="clearScales"> Очистить весы </button>
        <div class="remaining_weightings"> Осталось взвешиваний: {{ problemParams.weightings_amount }}</div>
        <div class="history" v-if="weightingHistory.length">
            <p v-for="(item, itemNum) in weightingHistory"> 
                <span style="font-weight: 600;"> Взвешивание {{ itemNum + 1 }}: </span> <br/>
                {{ item }} 
            </p>
        </div>
    </div>
    </div>
</template>

<script>
export default {
    props: ['problemParams', 'xhrData', 'newXhr'],
    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },
    data() {
        return {
            svgY: 0,
            svgHeight: 0,
            svgWidth: 0,
            scalesHeight: 0,
            scalesWidth: 0,
            cupCoordinates: {},
            weightCoordinates: [], //not important, declared in methods and mounted

            names: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
            nameYPad: 10,
            dragAreaMarginTop: 30,
            inRow: 5,
            rows: 2,
            weightGap: 15,
            weightHeight: 65,
            weightWidth: 65,
            containersGap: 20, //distance between containers in svg
            dropAllowDistance: 70, //svg distance
            
            targetWeight: {x: 0, y:0, index: undefined}, //current dragging object

            startAreaWeights: {},   
            answerAreaWeights: [],
            cupWeights: {'left': [], 'right': []},

            newSide: 'equal',
            weightMode: false,
            dragMode: false, //is drag?
        }
    },
    computed: {
        weightingHistory() {
            if (!this.problemParams.history)
                return []
            return this.problemParams.history
        },
        dragAreaWidth() {
            return this.inRow * (this.weightWidth + this.weightGap) + this.weightGap
        },
        dragAreaHeight() {
            return this.rows * (this.weightHeight + this.weightGap) + this.weightGap
        },
        answerAreaWidth() {
            return this.weightGap * 2 + this.weightWidth
        },
        answerAreaHeight(){
            return this.weightGap * 3 + this.weightWidth * 2
        },
        containersAreaWidth() {
            return this.dragAreaWidth + this.answerAreaWidth + this.containersGap
        }
    },
    watch: {
        newXhr(isNew) {  
            if (isNew) {
                this.$emit('xhrGet')
                if (this.xhrData.xhr_answer != this.newSide) {
                    this.newSide = this.xhrData.xhr_answer
                    this.weightMode = true
                }
            }            
        },
    },
    methods: {
        updateSvgCoordinates() {
            try {
                const svgRect = this.$refs['svg'].getBoundingClientRect()
                this.svgX = svgRect.left
                this.svgY = svgRect.top
                return true
            }
            catch(e) {
                return false
            }
        },
        updateCupCoordinates() {
            try {
                const cupCoordinates = {
                    left: {x: 0, y: 0},
                    right: {x: 0, y: 0},
                }
                const leftCupRect = document.querySelector('.left_cup').getBoundingClientRect()
                const rightCupRect = document.querySelector('.right_cup').getBoundingClientRect()
                cupCoordinates.left.x = leftCupRect.left + leftCupRect.width / 2 - this.svgX
                cupCoordinates.left.y = leftCupRect.top + leftCupRect.height / 2 - this.svgY
                cupCoordinates.right.x = rightCupRect.left + rightCupRect.width / 2 - this.svgX
                cupCoordinates.right.y = rightCupRect.top + rightCupRect.height / 2 - this.svgY
                this.cupCoordinates = cupCoordinates
                return true
            }
            catch(e) {
                return false
            }
        },
        inAllowedArea() { // if target object in allowed aarea
            const targetX = this.targetWeight.x + this.svgX
            const targetY = this.targetWeight.y + this.svgY
            console.log(targetX, targetY)
            if (targetX < 0 || targetX > window.innerWidth)
                return false
            if (targetY < 0 || targetY > window.innerHeight)
                return false
            return true
        },
        autoscroll(targetX, targetY) {
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
        getSvgHeight(scalesHeight) {
            this.svgHeight = scalesHeight + this.dragAreaHeight + this.dragAreaMarginTop
            this.scalesHeight = scalesHeight
        },
        getSvgWidth(scalesWidth) {
            this.scalesWidth = scalesWidth
            this.svgWidth = Math.max(scalesWidth, this.dragAreaWidth)
        },
        startWeight() {
            if (this.weightMode) {
                return
            }
            let leftCupWeights = []
            let rightCupWeights = []
            for (let weight of this.cupWeights.left) {
                leftCupWeights.push(weight.payload.index)
            }
            for (let weight of this.cupWeights.right) {
                rightCupWeights.push(weight.payload.index)
            }
            this.$emit('xhrRequest', {left: leftCupWeights, right: rightCupWeights})
        },
        stopWeight(currentSide) {
            this.weightMode = false
        },
        clearScales() {
            this.dragMode = false
            this.weightMode = false
            this.newSide = 'equal'
            for (const weight of this.cupWeights.left) {
                this.$set(this.startAreaWeights, weight.payload.index, true)
            }
            for (const weight of this.cupWeights.right) {
                this.$set(this.startAreaWeights, weight.payload.index, true)
            }
            this.$set(this.cupWeights, 'left', [])
            this.$set(this.cupWeights, 'right', [])
        },
        inRect(x, y, rect){
            if (x + this.svgX > rect.right || x + this.svgX < rect.left) {
                return false
            }
            if (y + this.svgY > rect.bottom || y + this.svgY < rect.top) {
                return false
            }
            return true
        },
        moveAt(x, y) {
            const svgUpdateStatus = this.updateSvgCoordinates()
            const cupUpdateStatus = this.updateCupCoordinates()
            if (!svgUpdateStatus || !cupUpdateStatus)
                return
            this.autoscroll(x, y)
            this.$set(this.targetWeight, 'x', x - this.svgX)
            this.$set(this.targetWeight, 'y', y - this.svgY)
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
            this.$set(this.targetWeight, 'index', index)
            this.moveAt(x, y)
        },
        drag(event) {
            if (!this.dragMode) {
                return
            }
            if (this.targetWeight.index == undefined)
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
        },
        endDrag() {
            if (!this.dragMode) {
                return
            }
            let cupToDrop = undefined
            let minDist = 10 ** 18
            for (const [cup, cupCoordinates] of Object.entries(this.cupCoordinates)) {
                const xDiff = Math.abs(cupCoordinates.x - this.targetWeight.x)
                const yDiff = Math.abs(cupCoordinates.y - this.targetWeight.y)
                const dist = Math.sqrt(xDiff ** 2 + yDiff ** 2)
                if (dist < minDist) {
                    minDist = dist
                    if (dist < this.dropAllowDistance) {
                        cupToDrop = cup
                    }
                }
            }
            const AnsContainerRect = this.$refs['ans_container'].getBoundingClientRect()
            if (this.inRect(this.targetWeight.x, this.targetWeight.y, AnsContainerRect)) {
                console.log('drop to ans area')
                this.dropToAnsArea()
            }

            else if(cupToDrop) {
                console.log('drop to cup')
                this.dropToCup(cupToDrop)
            }
            else {
                console.log('drop to drag area')
                this.backToStartArea()
            }
            this.dragMode = false
        },
        dropToAnsArea() {
            if (this.answerAreaWeights.length >= 2) {
                return
            }
            let newAnswerAreaWeights = JSON.parse(JSON.stringify(this.answerAreaWeights))
            newAnswerAreaWeights.push({
                index: this.targetWeight.index,
                html: this.$refs.choiced.innerHTML
            })
            console.log(newAnswerAreaWeights)
            this.answerAreaWeights = newAnswerAreaWeights
            let newAnswerAreaWeightsIndex = []
            for (const weight of newAnswerAreaWeights) {
                newAnswerAreaWeightsIndex.push(weight.index)
            }
            this.$emit('updateAnswer', newAnswerAreaWeightsIndex)
        },
        backToStartArea() {
            const dragIndex = this.targetWeight.index
            this.startAreaWeights[dragIndex] = true
        },
        dropToCup(cup) {
            let curCupWeights = this.cupWeights[cup]
            curCupWeights.push({
                html: this.$refs['choiced'].innerHTML, 
                payload: {index: this.targetWeight.index}
            })
            this.$set(this.cupWeights, cup, curCupWeights)
        },
        moveFromStartArea(index, event) {
            this.$set(this.startAreaWeights, index, false)
            this.startDrag(index, event)
        },
        moveFromCup(data) {
            const index = data.payload.index
            const cup = data.cup
            let newCupWeights = []
            for (const weightInfo of this.cupWeights[cup]) {
                if (weightInfo.payload.index != index) {
                    newCupWeights.push(weightInfo)
                }
            }
            this.$set(this.cupWeights, cup, newCupWeights)
            this.startDrag(index, window.event)
        },
        moveFromAnsArea(weight) {
            console.log(weight)
            let newAnswerAreaWeights = []
            for (const answerWeight of this.answerAreaWeights) {
                console.log(answerWeight.index, weight.index)
                if (answerWeight.index != weight.index) {
                    newAnswerAreaWeights.push(answerWeight)
                }
            }
            this.answerAreaWeights = newAnswerAreaWeights
            this.startDrag(weight.index, window.event)
        }
    },
    created() {
        let coordinates = []
        let startWeights = {}
        for (let row = 1; row <= this.rows; row++) {
            for (let column = 1; column <= this.inRow; column++) {
                coordinates.push({x: (column - 1) * (this.weightGap + this.weightWidth), y: 0})
                startWeights[(column - 1) + this.inRow * (row - 1)] = true
            }
        }
        this.weightCoordinates = coordinates
        this.startAreaWeights = startWeights
    },
    mounted() {
        document.addEventListener('mousemove', this.drag, {passive: false})
        document.addEventListener('touchmove', this.drag, {passive: false})
        document.addEventListener('touchend', this.endDrag)
        document.addEventListener('mouseup', this.endDrag)
    }
}
</script>
