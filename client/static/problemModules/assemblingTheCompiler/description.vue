<template>
	<div class="description">
		<div>
			У Васи сегодня экзамен по программированию, но (вот незадача!) компилятор его любимого языка сломался и не работает! 
			Помогите Васе и скомпилируйте программу – переведите ее в набор инструкций, понятный компьютеру. Компьютер понимает 
			базовые операции <b>Add, Sub, ShiftLeft, ShiftRight, Move</b> (описание операций см. ниже). Для вычислений обычно 
			используется восемь основных переменных (регистров), которые называются \(\mathtt{A}, \mathtt{B}, \mathtt{C}, \mathtt{D}, 
			\mathtt{E}, \mathtt{F}, \mathtt{G}, \mathtt{H}\). Однако в домашнем 
			задании можно использовать только регистры \(\mathtt{A}, \mathtt{B}, \mathtt{C}, \mathtt{D}\). Составьте из предложенных операций программу, которая будет 
			работать так же, как программа Васи. Возвращаемый результат необходимо положить в переменную \(\mathtt{A}\).
			Вот функция Васи:
		</div>
		<img class="function" src="/problem_assets/vasya_function.png" />
		<div>
			Значения чисел \(\mathtt{a}, \mathtt{b}, \mathtt{c}\) изначально сохранены в регистры \(\mathtt{A}, \mathtt{B}, \mathtt{C}\) соответственно.
			Количество строк в программе не должно превосходить \(\mathtt{10}\).
		</div>
		<div>
			<b><u>Описание команд:</u></b> <br/>
			<i>Далее буква \(\mathtt{T}\) может обозначать, как число, так и регистр:</i> <br/>
			<ol style="padding-top:1em; margin-left: 2em">
				<li><b>Add \(\mathtt{T}\), \(\mathtt{X}\)</b> – добавляет значение \(\mathtt{T}\) к значению 
					регистра \(\mathtt{X}\), результат сохраняется в регистре \(\mathtt{X}\)</li>
				<li><b>Sub \(\mathtt{T}\), \(\mathtt{X}\)</b> – вычитает значение \(\mathtt{T}\)
					из значения регистра \(\mathtt{X}\), результат сохраняется в регистре \(\mathtt{X}\)</li>
				<li><b>ShiftLeft \(\mathtt{T}\), \(\mathtt{X}\)</b> – умножает \(\mathtt{X}\) на \(\mathtt{2}^\mathtt{T}\)</li>
				<li><b>ShiftRight \(\mathtt{T}\), \(\mathtt{X}\)</b>  – в \(\mathtt{X}\) записывается целая часть 
					при делении \(\mathtt{X}\) на \(\mathtt{2}^\mathtt{T}\)</li>
				<li><b>Move \(\mathtt{T}\), \(\mathtt{X}\)</b> – значение в регистре \(\mathtt{X}\) становится равно значению \(\mathtt{T}\)</li>
			</ol>
		</div>
	</div>
</template>

<script>
export default {
	props: ['problemParams']
}
</script>

<style scoped>
img.function {
	width: 60%;
	height: auto;
	align-self: center;
}

.description {
	display: flex;
	flex-direction: column;
	gap: 1em;
}
</style>