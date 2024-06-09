<template>
    <svg version="1.1" :width="`${svgWidth}`" 
        :height="`${svgHeight}`" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <ScalesDefs />
        <g class="scales" :transform="`translate(${cupInnerRadiusX} 0)`">
            <g class="plank_with_cups" :transform="`translate(0 ${horizontalPlankMarginTop})`">
                <rect class="plank" 
                            x="0"
                            y="0"
                            :width="`${horizontalPlankWidth}`"
                            :height="`${horizontalPlankHeight}`" />
                <CupWithRope class="left_cup" :transform="`translate(0 ${horizontalPlankHeight / 2})`" v-bind="$attrs"></CupWithRope>
                <CupWithRope class="right_cup" :transform="`translate(${horizontalPlankWidth} ${horizontalPlankHeight / 2})`" :cupWidth="cupWidth" :cupInnerRadiusX="cupInnerRadiusX" 
                            :cupInnerRadiusY="cupInnerRadiusY" :cupOuterRadiusX="cupOuterRadiusX" 
                            :cupOuterRadiusY="cupOuterRadiusY" :hingeR="hingeR" :ropeHight="ropeHight" :ropeWidth="ropeWidth"></CupWithRope>
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
    </svg>
</template>

<style>
@import "./Scales.css" 
</style>

<script>
import CupWithRope from './components/CupWithRope.vue'

export default {
    components: {
        CupWithRope,
    },
    data() {
        return {
            cupInnerRadiusX: 80,
            cupInnerRadiusY: 40,
            cupOuterRadiusY: 70,
            horizontalPlankWidth: 500,
            horizontalPlankHeight: 10,
            horizontalPlankMarginTop: 10,
            verticalPlankWidth: 15,
            verticalPlankHeight: 400,
            baseWidth: 250,
            baseHeight: 80,
            baseInnerRadiusX: 90,
            hingeR: 6,
            ropeHight: 200,
            ropewidth: 2,
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
            return this.cupWidth + this.horizontalPlankWidth
        },
        svgHeight() {
            return this.verticalPlankHeight + this.baseHeight + this.baseOuterRadiusY 
        },
    },
}
</script>