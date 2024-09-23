<template>
	<div v-if="isListNotEmpty" class="submit_form_plot">
		<div class="update_button" role="button" @click="$emit('update')"> Обновить </div>
		<div class="submit_table">
			<span 
				v-for="header in tableHeaders" :key="header.id"
				class="table_header_item">
				{{ header.title }}
			</span>
			<template
				v-for="(submitElem, rowIndex) in runList">
				<div 
					v-for="(value, key, columnIndex) in submitElem.data" :key="`table_item_${rowIndex}_${columnIndex}`"
					class="table_item">
					{{ submitElem.data[tableHeaders[columnIndex].id] }}
				</div>
			</template>
		</div>
	</div>
</template>


<script>
export default {
	props: {
		runList: {
			type: Array,
			default: () => { return [] }
		}
	},

	data() {
		// console.log(this.runList)
		// console.log(this.runList[0].data.lang)
		return {
			tableHeaders: [
				{ title: 'Время посылки', id: 'submit_time'	},
				{ title: 'Компилятор', id: 'lang' },
				{ title: 'Память', id: 'size' },
				{ title: 'Время', id: 'duraction' },
				{ title: 'Вердикт', id: 'status' },
				{ title: 'Тест', id: 'tests_passed' },  
			],
		}
	},

	computed: {
		isListNotEmpty() {
			return this.runList.length
		}
	}
}
</script>