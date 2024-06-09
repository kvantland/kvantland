<template>
    <g>
        <g class="cup" :transform="`translate(0 ${ropeHight})`">
            <path class="outside" :d="`
                        M  ${-cupOuterRadiusX} 0 
                        a ${cupOuterRadiusX} ${cupOuterRadiusY} 0 0 0 ${cupWidth} 0
                        H 0`" />
            <ellipse class="inside" 
                        cx="0"
                        cy="0"
                        :rx="`${cupInnerRadiusX}`"
                        :ry="`${cupInnerRadiusY}`" />
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
    },
}
</script>