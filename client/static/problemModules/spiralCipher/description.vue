<template>
	<div class="description">
		<p>Вася загадал некоторое слово длины \(N\) и записал его по спирали (в направлении по часовой стрелке) в таблицу \( K \times L \).
		Затем он составил шифр из строк полученной таблицы (к слову, которое образуется буквами в первой строке, он дописал 
		справа аналогичное слово для второй строки, затем третьей и т.д.). 
		Напишите программу, которая смогла бы дешифровать любое закодированное слово.</p>
		<InputExamplesTable :inputExamples="inputExamples"></InputExamplesTable>
		<p>	<b>Входные данные: </b> <br>
			На первой строке через пробел вводятся два натуральных числа: \(K\) и \(L\). 
			На следующей строке вводится строка, состоящая из \(K \times L\) символов.
			Гарантируется, что \(K \times L \leq 100 000.\) 
		</p>
		<p> <b>Выходные данные:</b> строка длины \(K \times L\).</p>
	</div>
</template>


<script>
import InputExamplesTable from '../components/InputExamplesTable.vue';

export default {
	comments: {
		InputExamplesTable,
	},

	data() {
		return {
			inputExamples: [
				{
					input: ['3 3', 'kvandnalt'],
					output: ['kvantland'],
				},
			]
		}
	}
}
</script>

<style scoped>
.description {
	display: inline-flex;
	flex-direction: column;
	width: 100%;
	gap: 10px;
}
</style>