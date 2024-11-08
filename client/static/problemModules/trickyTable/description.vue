<template>
	<ClientOnly>
		<p>
			Заполните таблицу \(3 \times 3\) различными натуральными числами от \(1\) до \(200\) так, 
			чтобы произведения чисел в каждой строке и каждом столбце были одинаковы 
			(все шесть произведений) и одно из чисел в таблице было равно \({{ numberValue }}\).
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
		numberValue() {
			return this.problemParams.numberValue
		}
	}
}
</script>