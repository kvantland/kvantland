<template>
    <svg version="1.1" :width="`${svgWidth}`" 
        :height="`${svgHeight}`" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <g v-for="rowNum in (side * 2 - 1)" class="lamps_row" :transform="`translate(${Math.abs(side - rowNum) * lampRadius} ${(rowNum - 1) * lampRadius * Math.sqrt(3)})`">
        <circle v-for="lampNum in (side * 2 - Math.abs(side - rowNum) - 1)" :class="`lamp ${lamps[rowNum - 1][lampNum - 1] ? 'on' : 'off'}`" @click="switchLamp(rowNum, lampNum)"
            :cy="lampRadius" :cx="lampRadius * 2 * (lampNum - 1) + lampRadius" :r="lampRadius" />
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
        const side = this.problemParams.side
        console.log(side)
        const lampRadius = 10
        let lamps = []
        for (let row = 0; row < side * 2 - 1; row++)
            lamps.push(Array( side * 2 - 1 - Math.abs(side - row - 1)).fill().map((_, i) => {return 0}))
        return {
            lampRadius: 30,
            side: side,
            lamps: lamps,
        }
    },
    computed: {
        svgWidth() {
            return  (2 * this.side - 1) * this.lampRadius * 2
        },
        svgHeight() {
            return  2 * (this.side - 1) * this.lampRadius * Math.sqrt(3) + this.lampRadius * 2
        },
    },
    methods: {
        switchLamp(yInd, xInd) {
            this.$set(this.lamps[yInd - 1], xInd - 1, 1 - this.lamps[yInd - 1][xInd - 1])
            this.$emit('updateAnswer', this.lamps)
            console.log(this.lamps)
        }
    },
    mounted() {
        console.log(this.lamps)
    }
}
</script>

<style scoped>
.lamp {
    stroke: grey;
    stroke-width: 1px;
    cursor: pointer;
}

.lamp.on {
    fill: yellow;
}

.lamp.off {
    fill: white;
}
</style>