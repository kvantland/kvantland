<template>
    <div class="plot_area">
    <svg version="1.1" :width="`${boardWidth + paletteInd + colorCircleRadius * 2 * paletteColumns + paletteColumnInd + (paletteColumns - 1)}`" 
        :height="`${boardHeight}`" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <g class="board">
            <line class="horizontal" v-for="(line, num) in rectInColumn  + 1" 
                x1="0" :y1="`${side * num}`" :x2="`${rectInRow * side}`" :y2="`${side * num}`" :stroke-width="lineWidth" />
            <line class="vertical" v-for="(line, num) in rectInRow + 1"
                :x1="`${side * num}`" y1="0" :x2="`${side * num}`" :y2="`${rectInColumn * side}`" :stroke-width="lineWidth" />
            <g v-for="(rect_row, yInd) in rectInColumn" :key="`row_${yInd}`">
                <rect :class="['field', 'color-' + colors[yInd][xInd]]" v-for="(rect, xInd) in rectInRow" @click="paint(xInd, yInd)"
                    :x="`${xInd * side + rectInd}`" :y="`${yInd * side + rectInd}`" :width="innerSide" :height="innerSide" :key="`rect_${xInd}_${yInd}`"/>
                <text v-for="(perimeterValue, xInd) in problemParams.start_board[yInd]" :x="`${xInd * side + rectInd + side / 2}`" 
                    :y="`${yInd * side + rectInd + side / 2}`"> {{ perimeterValue }} </text>
            </g>
        </g>
        <g class="palette" :transform="`translate(${boardWidth + paletteInd} ${side / 2})`">
            <g class="paletteColumns" v-for="(column, columnNum) in paletteColumns" 
                :transform="`translate(${columnNum * (paletteColumnInd + 2 * colorCircleRadius) + colorCircleRadius} 0)`">
                <g v-for="(color, colorNum) in colorsInColumn" @click="chooseColor(colorNum + columnNum * colorsInColumn)" 
                    :transform="`translate(0 ${colorNum * side})`">
                    <circle :class="`color color-${colorNum + columnNum * colorsInColumn}`" cx="0" cy="0" :r="colorCircleRadius"  />
                    <text v-if="currentColor == colorNum + columnNum * colorsInColumn" x="0" y="0"> ✔️ </text>
                </g>
            </g>
        </g>
    </svg>
    </div>
</template>

<script>
export default {
    props: ["problemParams"],
    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },
    data() {
        const rectInRow = this.problemParams['start_board'].length
        const rectInColumn = this.problemParams['start_board'][0].length
        let colors = Array(rectInColumn).fill().map((_, i) => Array(rectInRow))
        return {
            rectInColumn: rectInColumn,
            rectInRow: rectInRow,
            side: 80,
            lineWidth: 2,
            paletteInd: 120,
            paletteColumns: 2,
            paletteColumnInd: 40,
            colorsInColumn: 5,
            colorCircleRadius: 30,
            currentColor: null,
            colors: colors,
        }
    },

    methods: {
        chooseColor(colorNum) {
            if(this.currentColor == colorNum)
                this.currentColor = null
            else 
                this.currentColor = colorNum
        },
        paint(xInd, yInd) {
            this.$set(this.colors[yInd], xInd, this.currentColor)
            this.$emit('updateAnswer', this.colors)
        }
    },

    computed: {
        boardWidth() {
            return this.rectInRow * this.side
        },
        boardHeight() {
            return this.rectInColumn * this.side + this.lineWidth
        },
        innerSide(){
            return this.side - this.lineWidth
        },
        rectInd() {
            return this.lineWidth / 2
        },
    },
    mounted() {
        console.log(this.colors)
    }
}
</script>