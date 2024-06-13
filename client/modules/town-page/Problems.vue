<template>
<g class="problems">
	<NuxtLink v-for="prb in problems_data" :to="`/problem/${prb.variantID}/`" :class="`level level_${prb.status}`" :transform="`translate(${prb.x} ${prb.y})`" :key="`problem_${prb}`"><title>{{prb.name}}</title>
		<circle class="level-icon" r="0.65em" />
		<text class="level-value" dy="0.35em">{{prb.points}}</text>
    </NuxtLink>
</g>
</template>
<script>
export default {
    props: ['problems_data']
}
</script>
<style scoped>
.level {
    text-anchor: middle;
    font-size: 60px;
    font-weight: bold;

    fill: currentColor;
    stroke-width: 2px;
    font-family: Montserrat Alternates
}

.level-value {
    stroke: inherit;
}

.level_open:hover {
    color: #ffe488;
    stroke: #9b785c;
}

.level_open {
    color: #ffc400;
    stroke: #b36d2a;
}

.level_solved {
    color: #77cc33;
    stroke: #339900;
}

.level_solved:hover {
    color: #99dd44;
    stroke: #55aa33;
}

.level_failed {
    color: #dd5533;
    stroke: #993300;
}

.level_failed:hover {
    color: #ee6644;
    stroke: #aa4433;
}
</style>