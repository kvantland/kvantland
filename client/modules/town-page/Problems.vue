<template>
<g class="problems">
	<a v-for="prb in data" :xlink:href="`/problem/${prb.variantID}/`" :class="`level level_${prb.status}`" :transform="`translate(${prb.x} ${prb.y})`"><title>{{prb.name}}</title>
		<circle class="level-icon" r="0.65em" />
		<text class="level-value">{{prb.points}}</text>
	</a>
</g>
</template>
<script>
export default {
    props: ['data']
}
</script>