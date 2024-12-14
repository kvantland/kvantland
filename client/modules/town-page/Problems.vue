<template>
	<g class="problems">
		<NuxtLink
			v-for="prb in problemsData" 
			:key="`problem_${prb.variantID}`" 
			:to="`/class/${classValue}/problem/${prb.variantID}/`" 
			:class="`level level_${prb.status}`" 
			:transform="`translate(${positions[prb.variantID].x} ${positions[prb.variantID].y})`">

			<title>{{prb.name}}</title>
			<circle class="level-icon" r="0.65em" />
			<text class="level-value" dy="0.35em">{{prb.points}}</text>
			</NuxtLink>
	</g>
</template>
<script>
export default {
    props: {
			problemsData: {
				type: Array,
				default: () => []
			},
			classValue: {
				type: String,
				default: 'all'
			}
		},
		computed: {
			positions() {
				const sortedPostions = JSON.parse(JSON.stringify(this.problemsData))
					.sort((problem1, problem2) => problem1.points - problem2.points)
				const center = {x: 1280 / 2, y: 720 / 2 }
				const radius = 250
				const startAngle = Math.PI / 2
				const vertexAmount = sortedPostions.length
				const addAngle = Math.PI * 2 / vertexAmount
				const positions = {}

				if (vertexAmount === 1) {
					positions[sortedPostions[0].variantID] = center
				}
				else {
					let angle = startAngle
					for (let vertexNum = 0; vertexNum < vertexAmount; vertexNum++) {
						const position = {x: center.x + radius * Math.cos(angle),
							y: center.y - radius * Math.sin(angle)}
						positions[sortedPostions[vertexNum].variantID] = position
						angle += addAngle
					}
				}
				console.log(positions)
				return positions
			}
		}
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