<template>
	<section v-if="tableRows.length" class="test-groups__section">
		<div class="notation">
			<p class="notation__header"> <b> Замечание: </b> </p>
			<p class="notation__description"> 
				В этой задаче можно набрать частичные баллы. 
				Для этого решение должно пройти все тесты одной 
				подгруппы с дополнительными условиями (баллы за 
				разные подгруппы суммируются):
			</p>
		</div>
		<table class="test-group-table">
			<thead class="test-group-table__test-group-table-head">
				<th class="test-group-table-head__item">Ограничение на подгруппу</th>
				<th class="test-group-table-head__item">Квантики за подгруппу</th>
			</thead>
			<tbody class="test-group-table__test-group-table-body">
				<tr 
					v-for="(tableRow, tableRowNum) in tableRows" :key="`test-group-table-body__test-group-table-row_num-${tableRowNum}`"
					class="test-group-table-body__test-group-table-row">
					<td class="test-group-table-row__item test-group-table-row__item_description">{{ tableRow.description }}</td>
					<td class="test-group-table-row__item test-group-table-row__item_cost">{{ tableRow.cost }}</td>
				</tr>
			</tbody>
		</table>
	</section>
</template>

<script>
export default {
	props: {
		tableRows: {
			type: Array,
			default: () => [],
		}
	},
	setup(props) {
		return props.tableRows
	}
}
</script>

<style lang="scss" scoped>
.test-groups__section {
	display: inline-flex;
	flex-direction: column;
	gap: 0.5em;
}
.notation {
	display: inline-flex;
	flex-direction: column;
}
.test-group-table {
	border-collapse: collapse;
}
.test-group-table-row__item {
	width: 50%;
	padding: 0.2em 0;
	border-top: 2px solid #6B6B6B80;
	&_cost {
		text-align: center;
	}
	&:first-child {
		border-right: 4px solid #6B6B6B80;
	}
}
.test-group-table-head__item {
	padding: 0.3em 0;
	border-bottom: 4px solid #6B6B6B80;
	font-weight: 600;
	&:first-child {
		border-right: 4px solid #6B6B6B80;
	}
}
</style>