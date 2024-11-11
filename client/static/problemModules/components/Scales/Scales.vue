<template>
    <g>
        <ScalesDefs />
        <g :transform="`scale(${scale})`" class="scaling">
            <g class="scales" :transform="`translate(${cupInnerRadiusX} 0)`">
                <g class="plank_with_cups" :transform="`translate(0 ${horizontalPlankMarginTop}) rotate(${angle} ${horizontalPlankWidth / 2} ${horizontalPlankHeight / 2})`">
                    <rect
											class="plank" style="fill: url(#blankShadow);	stroke: #976B38; stroke-width: 2;"
                                x="0"
                                y="0"
                                :width="`${horizontalPlankWidth}`"
                                :height="`${horizontalPlankHeight}`" />
                    <g ref="left_cup" :transform="`translate(0 ${horizontalPlankHeight / 2}) rotate(${-angle})`">
                        <CupWithRope
													class="left_cup_with_rope" :name="'left_cup'" :objects="leftCupObjects"
																		:object-side="itemSide"
																		:object-scale="objectScale"
																		:objects-to-center-scale="centerScale"
                                    :cup-width="cupWidth" :cup-inner-radius-x="cupInnerRadiusX" :cup-inner-radius-y="cupInnerRadiusY"
                                    :cup-outer-radius-x="cupOuterRadiusX" :cup-outer-radius-y="cupOuterRadiusY" 
                                    :hinge-r="hingeR" :rope-hight="ropeHight" :rope-width="ropeWidth" @moveFromCup="moveFromCup">
                        </CupWithRope>
                    </g>
                    <g ref="right_cup_with_rope" :transform="`translate(${horizontalPlankWidth} ${horizontalPlankHeight / 2}) rotate(${-angle})`">
                        <CupWithRope
												class="right_cup_with_rope"
													ref="right_cup" :name="'right_cup'"
													:object-side="itemSide"
													:object-scale="objectScale"
													:objects-to-center-scale="centerScale"
													:objects="rightCupObjects" :cup-width="cupWidth" :cup-inner-radius-x="cupInnerRadiusX"
													:cup-inner-radius-y="cupInnerRadiusY" 
													:cup-outer-radius-x="cupOuterRadiusX" :cup-outer-radius-y="cupOuterRadiusY"
													:hinge-r="hingeR" :rope-hight="ropeHight" :rope-width="ropeWidth" @moveFromCup="moveFromCup">
                        </CupWithRope>
                    </g>
                </g>
                <g class="base_with_plank" :transform="`translate(${horizontalPlankWidth / 2} 0)`">
                    <g class="basement" :transform="`translate(${-baseWidth / 2} ${verticalPlankHeight})`">
                        <path
													class="base_outside" style="stroke: #86755B; stroke-width: 2; fill: url(#baseBlankShadow);"
                                :d="`M 0 0 
                                V ${baseHeight}
                                a ${baseOuterRadiusX} ${baseOuterRadiusY} 0 0 0 ${baseWidth} 0
                                V 0
                                H 0`" />
                        <g class="base_top" :transform="`translate(${baseWidth / 2} 0)`" style="fill: #B68645; stroke: #976B38;	stroke-width: 2;">
                            <ellipse
															class="base_outside_top" style="fill: url(#baseBlankShadow);"
                                    cx="0"
                                    cy="0"
                                    :rx="`${baseOuterRadiusX}`"
                                    :ry="`${baseOuterRadiusY}`" />
                            <ellipse
															class="base_inside_top"
                                    cx="0"
                                    cy="0"
                                    :rx="`${baseInnerRadiusX}`"
                                    :ry="`${baseInnerRadiusY}`" />
                        </g>
                    </g>
                    <path 
														class="base_plank" style="fill: url(#baseBlankShadow); stroke: #976B38; stroke-width: 2;"
                            :transform="`translate(${-verticalPlankWidth / 2} 0)`"
                            :d="`M 0 0
                            V ${verticalPlankHeight}
                            A ${verticalPlankWidth / 2} ${verticalPlankWidth / 2 * ellipseAlpha} 0 0 0 ${verticalPlankWidth} ${verticalPlankHeight}
                            V 0
                            A ${verticalPlankWidth / 2} ${verticalPlankWidth / 2 * ellipseAlpha} 0 0 0 0 0`"/>
                    <circle 
												class="hinge" style="fill: #A7763D; stroke: #815A30; stroke-width: 4;"
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
    components: {
        CupWithRope,
    },
    props: {
        moveTo: {
					type: String,
					default: 'equal'
				}, // weaviest side
        scale: {
					type: Number,
					default: 1
				},
        rightCupObjects: {
					type: Array,
					default: () => [], // in format {html: '', payload: ''}
				},
        leftCupObjects: {
					type: Array,
					default: () => [],
				},
				target: {
					type: Object, // in format {x: Number, y: Number}
					default: () => {}
				},
				itemSide: {
					type: Number,
					default: 0,
				},
				objectScale: {
					type: Object,
					default: () => { return {x: 1, y: 1} },
				},
				centerScale: {
					type: Number,
					default: 0.7
				}
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
				return (this.cupWidth + this.horizontalPlankWidth) * this.scale // 680
			},
			svgHeight() {
				return (this.verticalPlankHeight + this.baseHeight + this.baseOuterRadiusY ) * this.scale
			},
			targetStr() {
				return this.target.x + ' ' + this.target.y
			},
    },
    watch: {
				targetStr() {
					const leftCupRect = document.querySelector('.left_cup_with_rope').getBoundingClientRect()
					const rightCupRect = document.querySelector('.right_cup_with_rope').getBoundingClientRect()
					if (this.inRect(this.target, leftCupRect)) {
						this.$emit('updateNearestCup', "left")
					}
					else if (this.inRect(this.target, rightCupRect)) {
						this.$emit('updateNearestCup', "right")
					}
					else {
						this.$emit('updateNearestCup', undefined)
					}
				},
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
    created() {
        this.$emit('svgHeight', this.svgHeight)
        this.$emit('svgWidth', this.svgWidth)
    },
    mounted() { 
    },
    methods: {
			inRect(target, rect) {
				if (target.x < rect.left || target.x > rect.right) {
					return false;
				}
				if (target.y < rect.top || target.y > rect.bottom) {
					return false;
				}
				return true;
			},
			moveFromCup(data) {
					this.$emit('moveFromCup', {itemHTML: data.itemHTML, itemIndex: data.itemIndex, cup: data.cup})
			}
    }
}
</script>