<template>
	<div class="content__wrapper">
		<p class="content__header"> Вердикты тестирования </p>
		<div class="codes-table">
			<div class="codes-table__codes-table-row_title codes-table__codes-table-row">
				<div 
					v-for="(header, headerNum) in tableHeaders" :key="`codes-table-header-row__item_num-${headerNum}`"
					 class="codes-table-header-row__item">
					 {{ header }}
				</div>
			</div>
			<div 
				v-for="(tableRow, tableRowNum) in tableRows" :key="`codes-table__codes-table-row_num-${tableRowNum}`" 
				:class="`codes-table__codes-table-row codes-table__codes-table-row_odd-${tableRowNum % 2}`">
				<div 
					v-for="(tableRowItem, tableRowItemNum) in tableRow" :key="`codes-table-row__item_num-${tableRowItemNum}_row-${tableRowNum}`"
					class="codes-table-row__item">
					{{ tableRowItem }}
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const tableHeaders = ref([
	'Код',
	'Когда возникает',
	'Возможная причина',
])

const tableRows = ref([
	{
		status: "OK",
		meaining: "Решение зачтено",
		reason: "Программа работает верно"
	},
	{
		status: "CE",
		meaining: "Компиляция программы завершилась с ошибкой",
		reason: `В программе допущена синтаксическая или семантическая ошибка. 
		Или неправильно указан язык программирования. Примечание: за попытки, 
		завершившиеся "ошибкой компиляции", штрафное время не начисляется`
	},
	{
		status: "WA",
		meaining: "Ответ не верен",
		reason: "Неверный алгоритм или Ошибка в реализации"
	},
	{
		status: "PE",
		meaining: `Программа проверки не может проверить выходные 
				данные, так как их формат не соответствует описанному`,
		reason: `Неверный формат вывода. Например, программа не печатает 
				результат или производит лишний вывод. Данный вердикт может 
				не использоваться, а ошибки подобного рода будут указываться 
				как Wrong answer.`
	},
	{
		status: "TL",
		meaining: `Программа превысила установленный в условии лимит времени`,
		reason: `Ошибка в программе (например, бесконечный цикл) или неэффективное решение`
	},
	{
		status: "ML",
		meaining: `Программа превысила установленный в условии лимит памяти`,
		reason: `Ошибка в программе (например, бесконечная рекурсия) или 
				неэффективное по размеру используемомй памяти решение`
	},
	{
		status: "RT",
		meaining: `Программа завершила работу с ненулевым кодом возврата`,
		reason: `Ошибка выполнения, например, деление на 0, корень из отрицательного 
				числа, выход за границу массива. Или программа на языке C/C++ не 
				завершается оператором return 0.`
	}

])
</script>

<style lang="scss" scoped>
.content__wrapper {
	display: inline-flex;
	flex-direction: column;
	gap: 40px;
	padding: 40px;
	border: 3px #1E8B93 solid;
	border-radius: 40px;
}
.content__header {
	color: #1E8B93;
	font-size: 40px;
	font-family: Montserrat Alternates;
	font-weight: 600
}
.codes-table {
	display: inline-flex;
	flex-direction: column;
	justify-content: stretch;
	font-size: 20px;

	.codes-table__codes-table-row {
		display: grid;
		grid-template-columns: 0.5fr 2.5fr 3fr;
		column-gap: 20px;
		padding: 20px;

		&_odd-1 {
			background-color: #edebeb;
			border-radius: 4px;
		}
	}
	.codes-table__codes-table-row_title {
		font-weight: 600;
		border-bottom: 1px black solid;
		padding-bottom: 20px;
	}
}

@media screen and (max-width: 800px) {
	.content__header {
		font-size: 20px;
	}
	.codes-table {
		font-size: 12px;
	}
	.content__wrapper {
		padding: 10px;
		gap: 20px;
		border-radius: 6px;
		border-width: 2px;
	}
	.codes-table .codes-table__codes-table-row {
		column-gap: 5px;
		padding: 10px;
	}
}
</style>