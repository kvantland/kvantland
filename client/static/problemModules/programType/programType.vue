<template>
	<div class="program_plot">
		<div class="editor_area">
			<div class="editor_area_buttons">
				<div :class="['button', inputMode === 'text' ? 'active': 'passive']" @click="changeMode('text')"> Написать здесь </div>
				<div :class="['button', inputMode === 'file' ? 'active': 'passive']" @click="changeMode('file')"> Прикрепить файл </div>
				<div class="select_language"> 
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
					<p>Осталось {{ remainingTries }} </p>
				</div>
			</div>
		</div>
		<SendArea :run-list="runList" :available-language="availableLanguage" @update="updateRuns"></SendArea>
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
		}
	},

	data() {
		return {
			inputMode: 'file',
			fileName: 'Файл не выбран',
			availableLanguage: [],
			formData: {
				file_input: '',
				text_input: '',
				lang: "python3",
			},
			remainingTries: '100 попыток',
		}
	},

	async fetch() {
		this.availableLanguage = await this.$axios.$get('/api/program_available_languages')
	},

	computed: {
		runList() {
			return this.problemParams.run_list
		}
	},

	mounted() {
		document.removeEventListener('DOMContentLoaded', this.updateRuns())
		document.addEventListener('DOMContentLoaded', this.updateRuns())
	},

	beforeDestroy() {
		document.removeEventListener('DOMContentLoaded', this.updateRuns())
	},

	methods: {
		changeMode(mode) {
			this.inputMode = mode
		},
		updateFile(event) {
			const fileList = event.target.files
			this.fileName = fileList[0].name
			this.$set(this.formData, 'file_input', fileList[0])
		},
		updateText() {
			const textInput = this.$refs.text_input.value
			this.$set(this.formData, 'text_input', textInput)
		},
		changeLanguage(event) {
			this.$set(this.formData, 'lang', event.target.value)
		},
		submitForm(){
			this.$emit('xhrRequest', {'data': JSON.stringify(this.formData), 'type': "send"})
		},
		updateRuns() {
			this.$emit('xhrRequest', {'type': "update"})
		}
	},
}
</script>