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
				<span 
					v-for="(value, key, columnIndex) in submitElem.data" :key="`table_item_${rowIndex}_${columnIndex}`"
					class="table_item">
					<span
						v-if="tableHeaders[columnIndex].id === 'status'" 
						:class="trasformData(submitElem.data)[tableHeaders[columnIndex].id] in unsuccessStatus ? 'unsuccess_status' : 
						trasformData(submitElem.data)[tableHeaders[columnIndex].id] === 'OK' ? 'success_status' : 'status_color'">
					{{ trasformData(submitElem.data)[tableHeaders[columnIndex].id] }}
					</span>
					<template v-else>
						{{ trasformData(submitElem.data)[tableHeaders[columnIndex].id] }}
					</template>
		</span>
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
		},
		availableLanguage: {
			type: Array,
			default: () => { return [] }
		},
	},

	data() {
		// console.log(this.runList)
		// console.log(this.runList[0].data.lang)
		return {
			tableHeaders: [
				{ title: 'Время посылки', id: 'submit_time'	},
				{ title: 'Компилятор', id: 'lang' },
				{ title: 'Память', id: 'size' },
				{ title: 'Время', id: 'duration' },
				{ title: 'Вердикт', id: 'status' },
				{ title: 'Тест', id: 'tests_passed' },  
			],
			unsuccessStatus: ['CE', 'RT', 'TL', 'PE', 'WA', 'PT', 'DQ', 'SE', 'ML', 'RJ', 'SV', 'WT']
		}
	},

	computed: {
		isListNotEmpty() {
			return this.runList.length
		}
	},

	methods: {
		getLongLangName(shortName) {
			for (const item of this.availableLanguage) {
				if (item.shortName.toString() === shortName.toString()) {
					return item.longName
				}
			}
		},

		zeroFill(expression, length) {
			const string = expression.toString().trim()
			const currentLength = string.length
			const zeroNumber = length - currentLength
			return '0'.repeat(zeroNumber) + string
		},

		getMonthByNum(num) {
			const translateList = {
				1: 'янв',
				2: 'февр',
				3: 'март',
				4: 'апр',
				5: 'май',
				6: 'июнь',
				7: 'июль',
				8: 'авг',
				9: 'сент',
				10: 'окт',
				11: 'нояб',
				12: 'дек'
			}
			return translateList[num + 1]
		},

		customDateString(date) {
			const day = date.getDate()
			const month = this.getMonthByNum(date.getMonth())
			const year = date.getFullYear()
			const hour = this.zeroFill(date.getHours(), 2)
			const minute = this.zeroFill(date.getMinutes(), 2)
			const second = this.zeroFill(date.getSeconds(), 2)

			const sendTime = [hour, minute, second].join(':')
			const sendDate = [day, month, year].join(' ')
			return [sendDate, sendTime].join(', ')
		},

		trasformData(data) {
			const transformedData = {}
			let newElem
			for (const key in data) {
				const currentValue = data[key]
				switch(key) {
					case 'submit_time':
						newElem = this.customDateString(new Date(currentValue * 1000));
						break;
					case 'lang':
						newElem = this.getLongLangName(currentValue);
						break;
					case 'size':
						newElem = Math.round(currentValue / 1024 * 100) / 100 + ' Kb';
						break;		
					case 'duration':
						newElem = currentValue + ' ms';
						break;			
					default:
						newElem = currentValue
				}
				transformedData[key] = newElem
			}
			return transformedData
		}
	}
}
</script>