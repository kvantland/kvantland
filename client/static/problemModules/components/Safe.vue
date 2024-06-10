<template>
    <svg version="1.1" :width="svgWidth" :height="svgHeight" overflow="visible" 
        xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <defs>
            <linearGradient id="slotShadow" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="gray" />
            <stop offset="25%" stop-color="rgba(230, 230, 230, 1)" />
            <stop offset="100%" stop-color="gray" />
            </linearGradient>
        </defs>
        <g :transform="`translate(0 ${arrowsHeight + arrowsPad})`" class="safe_without_arrows"> 
            <rect class="outerRect" x="0" y="0" :width="outerRectWidth" :height="outerRectHeight" />
            <g :transform="`translate(${paddingLeft} ${paddingTop})`" class="slots_container">
                <rect class="innerRect" x="0" y="0" :width="innerRectWidth" :height="innerRectHeight" />
                <g class="slots" :transform="`translate(${gap} ${gap})`">
                    <svg v-for="(slot, slotNum) in slotsAmount" class="slot" :x="slotNum * (gap + slotWidth)" y="0" :width="slotWidth" :height="slotHeight" :key="`slot_${slotNum}`">
                        <rect class="slot_display" x="0" y="0" :width="slotWidth" :height="slotHeight" :fill="`url(#slotShadow)`" />
                        <g class="text" :transform="`translate(${slotWidth / 2} ${slotHeight / 2})`">
                            <svg x="0" :y="Math.sin(scrollAngles[slotNum] - Math.PI/5) * slotRadius" overflow="visible">
                                <text class="prev_number" :transform="`scale(1 ${Math.cos(scrollAngles[slotNum] - Math.PI/5)})`"> 
                                    {{ currentValues[slotNum][0] }} </text>
                            </svg>
                            <svg x="0" :y="Math.sin(scrollAngles[slotNum]) * slotRadius" overflow="visible">
                                <text class="current_number" :transform="`scale(1 ${Math.cos(scrollAngles[slotNum])})`">
                                    {{ currentValues[slotNum][1] }} </text>  
                            </svg>
                            <svg x="0" :y="Math.sin(scrollAngles[slotNum] + Math.PI/5) * slotRadius" overflow="visible">
                                <text class="next_number" :transform="`scale(1 ${Math.cos(scrollAngles[slotNum] + Math.PI/5)})`"> 
                                    {{ currentValues[slotNum][2] }} </text>
                            </svg>
                        </g>
                    </svg>
                </g>
            </g>
        </g>
        <g class="arrows" :transform="`translate(${paddingLeft + gap} 0)`">
            <path v-for="(slot, slotNum) in slotsAmount" v-if="startValues[slotNum] == '*'" :key="`arrow_up_${slotNum}`"
                :transform="`translate(${slotNum * (slotWidth + gap)} ${arrowsHeight})`" @click="scrollUp(slotNum)"
                :d="`M 0 0 h ${slotWidth} l ${-slotWidth/2},${-arrowsHeight/2} z`" class="up_arrow arrow" ></path>
            <path v-for="(slot, slotNum) in slotsAmount" v-if="startValues[slotNum] == '*'" @click="scrollDown(slotNum)" :key="`arrow_down_${slotNum}`"
                :transform="`translate(${slotNum * (slotWidth + gap)} ${arrowsHeight + arrowsPad * 2 + outerRectHeight})`"
                :d="`M 0 0 h ${slotWidth} l ${-slotWidth/2},${arrowsHeight/2} z`" class="down_arrow arrow"></path>
        </g>
    </svg>
</template>

<script>
export default {
    props: ['slotsAmount', 'startValues'],
    data() {
        let AngleArr = Array(this.slotsAmount).fill().map((_i) => {return 0})
        console.log(AngleArr)
        let currentValues = []
        for (const value of this.startValues) {
            if (value == '*')
                currentValues.push([9, '✱', 0])
            else
                currentValues.push([(value + 9) % 10, value, (value + 1) % 10])
        }
        return {
            slotWidth: 50,
            slotHeight: 100,
            gap: 3,
            paddingTop: 15,
            paddingLeft: 10,
            arrowsPad: 10,
            arrowsHeight: 35,
            scrollAngleSpeed: Math.PI/100,
            scrollMode: false,
            scrollAngles: AngleArr,
            currentValues: currentValues,
        }
    },
    computed: {
        outerRectWidth() {
            return (this.slotWidth + this.gap) * this.slotsAmount + this.gap + this.paddingLeft * 2
        },
        outerRectHeight() {
            return this.slotHeight + this.gap * 2 + this.paddingTop * 2
        },
        innerRectWidth() {
            return (this.slotWidth + this.gap) * this.slotsAmount + this.gap
        },
        innerRectHeight() {
            return this.slotHeight + this.gap * 2
        },
        svgHeight() {
            return this.outerRectHeight + (this.arrowsHeight + this.arrowsPad) * 2
        },
        svgWidth() {
            return this.outerRectWidth
        },
        slotRadius() {
            return Math.sin(Math.PI * 8/10/2) / Math.sin(2*Math.PI/10) * this.slotHeight
        },
        scrollTrigger() {
            return JSON.stringify(this.scrollAngles)
        },
    },
    methods: {
        scrollUp(num) {
            if (this.scrollMode) {return}
            this.scrollMode = true
            this.$set(this.scrollAngles, num, this.scrollAngles[num] - this.scrollAngleSpeed)
        },
        scrollDown(num) {
            if (this.scrollMode) {return}
            this.scrollMode = true
            this.$set(this.scrollAngles, num,  this.scrollAngles[num] + this.scrollAngleSpeed)
        },
    },
    watch: {
        scrollTrigger() {
            for (let slotNum=0; slotNum < this.slotsAmount; slotNum++) {
                if (this.scrollAngles[slotNum] == 0)
                    continue;
                setTimeout(function(){
                    if (Math.abs(this.scrollAngles[slotNum]) < Math.PI/5) {
                        if (this.scrollAngles[slotNum] > 0)
                            this.$set(this.scrollAngles, slotNum, this.scrollAngles[slotNum] + this.scrollAngleSpeed)
                        else
                            this.$set(this.scrollAngles, slotNum, this.scrollAngles[slotNum] - this.scrollAngleSpeed)
                    }
                    else {
                        if (this.scrollAngles[slotNum] >= Math.PI/5) {
                            const newValue = this.currentValues[slotNum][0]
                            this.$set(this.currentValues[slotNum], 1, newValue)
                            this.$set(this.currentValues[slotNum], 0, (newValue + 1) % 10)
                            this.$set(this.currentValues[slotNum], 2, (newValue + 9) % 10)
                        }
                        else {
                            const newValue = this.currentValues[slotNum][2] 
                            this.$set(this.currentValues[slotNum], 1, newValue)
                            this.$set(this.currentValues[slotNum], 0, (newValue + 1) % 10)
                            this.$set(this.currentValues[slotNum], 2, (newValue + 9) % 10)
                        }
                        this.$set(this.scrollAngles, slotNum, 0)
                        this.scrollMode = false
                        this.$emit('changeConfig', this.currentValues)
                    }
                }.bind(this), 10)
            }
        },
    },
}
</script>

<style scoped>

.arrow{
	fill:red;
	stroke: darkred;
}

.outerRect{
	fill:rgb(96,96,96);
}

text.number_value{
	font-family:Agency FB;
	font-size: 50px;
}
.innerRect{
    fill: black;
}

@media(hover:hover) and (pointer:fine) {
	.arrow:hover {
		cursor:pointer;
		fill:rgb(139, 0, 0);
	}
}

text{
	font-size: 30px;
	text-anchor: middle;
	dominant-baseline: central;
	font-family: inherit;
	font-weight: 1000
}
</style>