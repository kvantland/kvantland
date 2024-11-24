<template>
	<ClientOnly>
		<p>
			Поле для игры \( {{ boardWidth }} \times {{ boardHeight }} \). В одной угловой клетке находится фермер, в 
			другой - петушок, которого ловит фермер. Фермер и петух ходят по 
			очереди, за секунду каждый перемещается в соседнюю клетку. 
			Петух пойман, если после хода фермера он оказался в клетке с петухом.
			Поймайте петуха, если у вас не более \(30\) ходов.
		</p>
	</ClientOnly>
</template>

<script>
export default {
	props: {
		problemParams: {
			type: Object,
			default: () => {}
		}
	},
	computed: {
		boardWidth() {
			return this.problemParams.board_width
		},
		boardHeight() {
			return this.problemParams.board_height
		}
	}
}
</script>