<template>
	<p class="description">
		<ClientOnly>
			На поле \(6 \times 6\) растут яблони. 
			Огородите участок \(3 \times 3\), на котором растёт ровно \( {{ appleAmount }} \) {{ langForm }}.
		</ClientOnly> 
	</p>
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
		appleAmount() {
			return this.problemParams?.apple_amount
		},
		langForm() {
			const appleAmount = this.appleAmount
			if (appleAmount >= 3 && appleAmount <= 4) return "яблони";
			else return "яблонь"
		}
	}
}
</script>