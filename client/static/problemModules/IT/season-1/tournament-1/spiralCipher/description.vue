<template>
	<ProgramTypeDescription :input-examples="inputExamples">
		<ClientOnly>
		<p>Вася загадал некоторое слово и записал его по спирали (в направлении по часовой стрелке) в таблицу \( K \times L \).
		Затем он составил шифр из строк полученной таблицы (к слову, которое образуется буквами в первой строке, он дописал 
		справа аналогичное слово для второй строки, затем третьей и т.д.). 
		Напишите программу, которая смогла бы дешифровать любое закодированное слово.</p>
		<img class="spiral_cipher_image" style="width: 30%; align-self: center;" src="/problem_assets/spiral_cipher.png"/>
		<p>	<b>Входные данные: </b> <br>
			На первой строке через пробел вводятся два натуральных числа: \(K\) и \(L\). 
			На следующей строке вводится строка, состоящая из \(K \cdot L\) символов.
			Гарантируется, что \(K \cdot L \leq 100 000.\) 
		</p>
		<p> <b>Выходные данные:</b> строка длины \(K \cdot L\).</p>
		</ClientOnly>
	</ProgramTypeDescription>
</template>


<script>
import ProgramTypeDescription from '../../../common/programType/components/ProgramTypeDescription.vue';

export default {
	components: {
		ProgramTypeDescription,
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
