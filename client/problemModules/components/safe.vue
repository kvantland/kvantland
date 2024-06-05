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
            <g :transform="`translate(${paddingLeft} ${paddingTop})`" class="slots">
                <rect class="innerRect" x="0" y="0" :width="innerRectWidth" :height="innerRectHeight" />
                <svg v-for="slotNum in slotsAmount" class="slot" :x="slotNum * (gap + slotWidth)" y="0" :width="slotWidth" :height="slotHeight">
                    <rect class="slot_display" x="0" y="0" :width="slotWidth" :height="slotHeight" />
                    <text class="current_number" :x="slotWidth / 2" :y="slotHeight / 2"> {{ startValues[slotNum] }} </text>  
                    <text class="prev_number" :x="slotWidth / 2" :y="-slotHeight / 2"> {{ (startValues[slotNum] + 9) % 10 }} </text>
                    <text class="next_number" :x="slotWidth / 2" :y="slotHeight * 3 / 2"> {{ (startValues[slotNum] + 1) % 10 }} </text>
                </svg>
            </g>
        </g>
        <g class="arrows">
            <path v-for="slotNum in slotsAmount" 
                :d="`M 0 0 l ${-slotWidth/2},${-slotHeight/2} L 0 0`"
                "></path>
        </g>
    </svg>
</template>

<script>
export default {
    props: ['slotsAmount', 'startValues'],
    data() {
        const slotsAmount = this.slotsAmount
        return {
            slotWidth: 50,
            slotHeight: 100,
            gap: 2,
            paddingTop: 10,
            paddingLeft: 10,
            arrowsPad: 10,
            arrowsHeight: 10,
        }
    },
    computed: {
        outerRectWidth() {
            return this.slotWidth * this.slotsAmount + this.gap * 2 + this.paddingLeft * 2
        },
        outerRectHeight() {
            return this.slotHeight + this.gap * 2 + this.paddingTop * 2
        },
        innerRectWidth() {
            return this.slotWidth * this.slotsAmount + this.gap * 2
        },
        innerRectHeight() {
            return this.slotHeight + this.gap * 2
        },
        svgHeight() {
            return this.outerRectHeight + (this.arrowsHeight + this.arrowsPad) * 2
        },
        svgWidth() {
            return this.outerRectWidth
        }
    }

}
</script>