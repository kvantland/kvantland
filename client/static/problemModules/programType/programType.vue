<template>
	<div class="program_plot">
		<div class="code_instruction">
			Значения вердиктов тестирования:
			<NuxtLink to="/programCodesDescription" style="text-decoration: underline; color: blue"> ссылка </NuxtLink>
		</div>
		<div class="editor_area">
			<div class="editor_area_buttons">
				<div :class="['button', inputMode === 'text' ? 'active': 'passive']" @click="changeMode('text')"> Написать здесь </div>
				<div :class="['button', inputMode === 'file' ? 'active': 'passive']" @click="changeMode('file')"> Прикрепить файл </div>
				<div class="select_language"> 
					<p class="select_language_layout"> Язык: </p>
					<select :value="formData.lang" @change="changeLanguage($event)" >
						<option v-for="lang in availableLanguage" :key='`option_${lang.shortName}`' :value="lang.shortName">{{ lang.longName }}</option>
					</select>
				</div>
			</div>
			<div v-if="inputMode === 'text'" class="text_input" >
				<div class="textarea_wrapper">
					<textarea ref="text_input" @change="updateText()"></textarea>
				</div>
			</div>
			<div v-else-if="inputMode === 'file'" class="file_input">
				<div class="filearea_wrapper">
					<div class="status">
						<span><b>Выберите файл: </b></span>
						<span>{{ fileName }}</span>
					</div>
					<input id="program_upload" type="file"  @change="updateFile($event)">
					<label for="program_upload" class="input-file-btn"> Обзор... </label>
				</div>
			</div>
			<div class="send_button_area">
				<div class="send_button" @click="submitForm">Отправить</div>
				<div class="tries_area">
					<img class="attention" src="/problem_assets/attention.svg" />
					<p>Осталось попыток: {{ remainingTries }} </p>
				</div>
			</div>
		</div>
		<SendArea :run-list="reversedRunList" :available-language="availableLanguage" @update="updateRuns"></SendArea>
	</div>
</template>

<script>
import SendArea from './components/SendArea.vue';

export default {
	components: {
		SendArea,
	},

	props: {
		problemParams: {
			type: Object,
			default: () => {return {}}
		},
		newXhr: {
			type: Boolean,
			default: false,
		},
		xhrData: {
			type: Object,
			default: () => { return {} }
		}
	},
	
	data() {
		return {
			inputMode: 'file',
			fileName: 'Файл не выбран',
			availableLanguage: [],
			formData: {
				text_input: '',
				lang: "python3",
			},
			fileInput: '',
		}
	},

	async fetch() {
		this.availableLanguage = await this.$axios.$get('/api/program_available_languages')
	},

	computed: {
		runList() {
			return this.problemParams.run_list
		},
		remainingTries() {
			return this.problemParams.available_tries
		},
		reversedRunList() {
			if (this.runList) {
				return JSON.parse(JSON.stringify(this.runList)).reverse()
			}
			return []
		}
	},

	watch: {
		newXhr(isNew) {
			if (isNew) {
				this.$emit('xhrGet')
				if (this.xhrData.xhr_answer.display) {
					this.$emit('showXhrDialog', this.xhrData.xhr_answer.message)
				}
			}
		},
		runList(newRunList) {
			console.log(newRunList)
			const okIndex = this.getOkIndex(newRunList)
			console.log('ok index: ', okIndex)
			console.log('run list: ', newRunList)
			if (okIndex !== undefined) {
				setTimeout(function(){this.$emit('xhrRequest', {'type': 'update_status', 'index': okIndex})}.bind(this), 100)
			}
		}
	},

	mounted() {
		console.log('languages: ', this.availableLanguage)
		document.removeEventListener('DOMContentLoaded', this.updateRuns())
		document.addEventListener('DOMContentLoaded', this.updateRuns())
	},

	beforeDestroy() {
		document.removeEventListener('DOMContentLoaded', this.updateRuns())
	},

	methods: {
		changeMode(mode) {
			this.inputMode = mode
			if (mode === 'text') {
				this.fileInput = ''
				this.fileName = 'Файл не выбран'
			}
		},
		updateFile(event) {
			const fileList = event.target.files
			this.fileName = fileList[0].name
			this.fileInput = fileList[0]
		},
		updateText() {
			const textInput = this.$refs.text_input.value
			this.$set(this.formData, 'text_input', textInput)
		},
		changeLanguage(event) {
			this.$set(this.formData, 'lang', event.target.value)
		},
		submitForm(){
			console.log('data to send: ', this.formData)
			const dataToSend = new FormData();
			dataToSend.append('text_input', this.formData.text_input)
			dataToSend.append('file_input', this.formData.file_input)
			dataToSend.append('lang', this.formData.lang)
			console.log(dataToSend)
			this.$emit('xhrRequest', {'data': this.formData, 'type': "send", 'xhrFiles': [{'title': 'file_input', 'content': this.fileInput}]})
			//this.$emit('xhrRequest', {'data': dataToSend, 'type': "send"})
		},
		updateRuns() {
			this.$emit('xhrRequest', {'type': "update"})
		},
		getOkIndex(runList) {
			let index = 0
			for (const run of runList) {
				if (run.data.status === 'OK') {
					return index
				}
				index++
			}
			return undefined
		}
	},
}
</script>