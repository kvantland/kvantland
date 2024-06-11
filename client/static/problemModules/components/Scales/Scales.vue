<template>
    <g>
        <ScalesDefs />
        <g :transform="`scale(${scale})`" class="scaling">
            <g class="scales" :transform="`translate(${cupInnerRadiusX} 0)`">
                <g class="plank_with_cups" :transform="`translate(0 ${horizontalPlankMarginTop}) rotate(${angle} ${horizontalPlankWidth / 2} ${horizontalPlankHeight / 2})`">
                    <rect class="plank" 
                                x="0"
                                y="0"
                                :width="`${horizontalPlankWidth}`"
                                :height="`${horizontalPlankHeight}`" />
                    <g ref="left_cup" :transform="`translate(0 ${horizontalPlankHeight / 2}) rotate(${-angle})`">
                        <CupWithRope class="left_cup_with_rope" :name="'left_cup'" :objects="leftCupObjects"
                                    :cupWidth="cupWidth" :cupInnerRadiusX="cupInnerRadiusX" @moveFromCup="moveFromCup"
                                    :cupInnerRadiusY="cupInnerRadiusY" :cupOuterRadiusX="cupOuterRadiusX" 
                                    :cupOuterRadiusY="cupOuterRadiusY" :hingeR="hingeR" :ropeHight="ropeHight" :ropeWidth="ropeWidth">
                        </CupWithRope>
                    </g>
                    <g ref="right_cup_with_rope" :transform="`translate(${horizontalPlankWidth} ${horizontalPlankHeight / 2}) rotate(${-angle})`">
                        <CupWithRope :name="'right_cup'" :objects="rightCupObjects"
                                    :cupWidth="cupWidth" :cupInnerRadiusX="cupInnerRadiusX" ref="right_cup"
                                    :cupInnerRadiusY="cupInnerRadiusY" :cupOuterRadiusX="cupOuterRadiusX" @moveFromCup="moveFromCup"
                                    :cupOuterRadiusY="cupOuterRadiusY" :hingeR="hingeR" :ropeHight="ropeHight" :ropeWidth="ropeWidth">
                        </CupWithRope>
                    </g>
                </g>
                <g class="base_with_plank" :transform="`translate(${horizontalPlankWidth / 2} 0)`">
                    <g class="basement" :transform="`translate(${-baseWidth / 2} ${verticalPlankHeight})`">
                        <path class="base_outside"
                                :d="`M 0 0 
                                V ${baseHeight}
                                a ${baseOuterRadiusX} ${baseOuterRadiusY} 0 0 0 ${baseWidth} 0
                                V 0
                                H 0`" />
                        <g class="base_top" :transform="`translate(${baseWidth / 2} 0)`">
                            <ellipse class="base_outside_top"
                                    cx="0"
                                    cy="0"
                                    :rx="`${baseOuterRadiusX}`"
                                    :ry="`${baseOuterRadiusY}`" />
                            <ellipse class="base_inside_top"
                                    cx="0"
                                    cy="0"
                                    :rx="`${baseInnerRadiusX}`"
                                    :ry="`${baseInnerRadiusY}`" />
                        </g>
                    </g>
                    <path class="base_plank"
                            :transform="`translate(${-verticalPlankWidth / 2} 0)`"
                            :d="`M 0 0
                            V ${verticalPlankHeight}
                            A ${verticalPlankWidth / 2} ${verticalPlankWidth / 2 * ellipseAlpha} 0 0 0 ${verticalPlankWidth} ${verticalPlankHeight}
                            V 0
                            A ${verticalPlankWidth / 2} ${verticalPlankWidth / 2 * ellipseAlpha} 0 0 0 0 0`"/>
                    <circle class="hinge"
                        cx="0"
                        :cy="`${horizontalPlankMarginTop + horizontalPlankHeight / 2}`"
                        :r="`${hingeR * 2}`" />
                </g>
            </g>
        </g>
    </g>
</template>

<script>
import CupWithRope from './components/CupWithRope.vue'

export default {
    props: {
        moveTo: {default: 'equal'}, // weaviest side
        scale: {default: 1},
        rightCupObjects: {default: function(){return []}}, //in format {html: '', payload: ''}
        leftCupObjects: {default: function(){return []}},
    },
    components: {
        CupWithRope,
    },
    data() {
        return {
            cupInnerRadiusX: 120,
            cupInnerRadiusY: 50,
            cupOuterRadiusY: 90,
            horizontalPlankWidth: 500,
            horizontalPlankHeight: 10,
            horizontalPlankMarginTop: 20,
            verticalPlankWidth: 15,
            verticalPlankHeight: 400,
            baseWidth: 250,
            baseHeight: 80,
            baseInnerRadiusX: 90,
            hingeR: 8,
            ropeHight: 200,
            ropeWidth: 2,

            angleStep: 0.4,
            stopAngle: 20,
            angleSign: 1, // 1 or -1 - rotation sgn
            angle: 0,
        }
    },
    computed: {
        ellipseAlpha() {
            return this.cupInnerRadiusY / this.cupInnerRadiusX
        },
        cupOuterRadiusX() {
            return this.cupInnerRadiusX
        },
        cupWidth() {
            return this.cupInnerRadiusX * 2
        },
        baseOuterRadiusX() {
            return this.baseWidth / 2
        },
        baseOuterRadiusY() {
            return this.ellipseAlpha * this.baseOuterRadiusX
        },
        baseInnerRadiusY() {
            return this.baseInnerRadiusX * this.ellipseAlpha
        },
        svgWidth() {
            return (this.cupWidth + this.horizontalPlankWidth) * this.scale //680
        },
        svgHeight() {
            return (this.verticalPlankHeight + this.baseHeight + this.baseOuterRadiusY ) * this.scale
        },
    },
    watch: {
        moveTo(newSide, prevSide) {
            console.log(prevSide, newSide)
            if (newSide == 'left' || (prevSide == 'right' && newSide == 'equal')) {
                this.angleSign = -1
                this.angle += this.angleSign * this.angleStep
            }
            else if (newSide == 'right' || (prevSide == 'left' && newSide == 'equal')) {
                this.angleSign = 1
                this.angle += this.angleSign * this.angleStep
            }
            if (newSide == 'equal') {
                this.stopAngle = 0
            }
            else {
                this.stopAngle = 20
            }
        },
        async angle(newValue) {
            if (this.angleSign == 1 && newValue >= this.stopAngle) {
                this.$emit('stopMove', this.moveTo)
                return
            }
            else if (this.angleSign == -1 && newValue <=  -this.stopAngle) {
                this.$emit('stopMove', this.moveTo)
                return
            }
            setTimeout(function(){
                this.angle += this.angleSign * this.angleStep
            }.bind(this), 10)
        }
    },
    methods: {
        moveFromCup(data) {
            this.$emit('moveFromCup', {payload: data.payload, cup: data.cup})
        }
    },
    created() {
        this.$emit('svgHeight', this.svgHeight)
        this.$emit('svgWidth', this.svgWidth)
    },
    mounted() { 
    }
}
</script>

<style>
@import "./Scales.css" 
</style>