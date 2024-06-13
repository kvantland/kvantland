<template>
    <g>
        <g :class= "`cup ${name}`" :transform="`translate(0 ${ropeHight})`">
            <ellipse class="inside" 
                        cx="0"
                        cy="0"
                        :rx="`${cupInnerRadiusX}`"
                        :ry="`${cupInnerRadiusY}`" />
            <g class="objects" :transform="`scale(${objectsToCenterScale}) translate(0 ${objectMarginTop})`">
                <g v-for="(object, objectNum) in objects" v-html="object.html" class="object" @mousedown="moveFromCup(object.payload)"
                    :transform="`translate(${objectsCoordinates[objectNum].x} ${objectsCoordinates[objectNum].y})`"></g>
            </g>
            <path class="outside" :d="`
                        M  ${-cupOuterRadiusX} 0 
                        a ${cupOuterRadiusX} ${cupOuterRadiusY} 0 0 0 ${cupWidth} 0
                        A ${cupInnerRadiusX} ${cupInnerRadiusY} 0 0 1 ${-cupWidth / 2} 0 `" />
        </g>

        <g class="ropes">
            <line 
                x1="0"
                y1="0"
                :x2="`${-cupWidth / 2}`"
                :y2="ropeHight" />
            <line 
                x1="0"
                y1="0"
                x2="0"
                :y2="ropeHight + cupInnerRadiusY" />
            <line 
                x1="0"
                y1="0"
                :x2="`${cupWidth / 2}`"
                :y2="ropeHight" />
        </g>
            
        <circle class="hinge"
                    cx="0"
                    cy="0"
                    :r="`${hingeR}`"/>
	</g>
</template>

<script>
export default {
    props: {
        cupWidth: {},
        cupInnerRadiusX: {},
        cupInnerRadiusY: {},
        cupOuterRadiusX: {},
        cupOuterRadiusY: {},
        ropeHight: {},
        ropeWidth: {},
        hingeR: {},
        name: {default: ''},
        objects: {default: () => {return []}},
        objectMarginTop: {default: 4},
        objectsToCenterScale: {default: 0.7},
    },
    computed: {
        objectsCoordinates() {
            let coordinates = []
            let angle = 0
            const objectsAmount = this.objects.length
            const angleStep = Math.PI * 2 / objectsAmount
            for (let objectNum = 0; objectNum < objectsAmount; objectNum++) {
                angle += angleStep
                const x = this.cupInnerRadiusX * Math.cos(angle)
                const y = this.cupInnerRadiusY * Math.sin(angle)
                coordinates.push({x: x, y: y})
            }
            return coordinates
        }
    },
    methods: {
        moveFromCup(payload) {
            this.$emit('moveFromCup', {payload: payload, cup: this.name.split('_')[0]})
        }
    },
    created() {
        console.log(this.objects, this.name)
    },
}
</script>

<style scoped>
.object {
    cursor: grab;
}
</style>