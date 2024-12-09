<template>
	<div class="problem_container">
		<div class="problem_header">
			<p class="problem_title"> {{ title }} </p>
			<div class="problem_cost"> {{ cost }} </div>
		</div>

		<div class="problem_body">
			<div v-if="description" v-html="description"></div>
			<component :is="dynamicDescription" v-if="!description" :problem-params="variantParams" />
			<img v-if="image" class="problem_img" :src="image" />
			<div v-if="componentPath" ref="problem" class="problem newTypeProblem">
				<component 
					:is="dynamicProblemComponent" v-if="!answerGiven && dynamicProblemComponent" v-model="currentAnswer" :xhr-data="xhrData" 
					:new-xhr="newXhr"
					:confirm-action-result="confirmActionResult" :problem-params="variantParams" @xhrGet="xhrGet"
					@showXhrDialog="showXhrDialog" @showConfirmDialog="showConfirmDialog" @xhrRequest="xhrRequest" @updateProblemStatus="updateProblemStatus"/>
				<div v-if="answerGiven" class="problem_solution" v-html="solution"></div>
			</div>
			<div v-else-if="problemContent" class="problem oldTypeProblem" v-html="problemContent.problemHTML" />
			<HintContainer v-if="hint.description" :description="hint.description" />
		</div>

		<component :is="dynamicInput" v-if="!answerGiven && dynamicInput" :has-hint="hint.status" @sendAnswer="sendAnswer" @getHint="getHint"/>
		<ProblemResult 
			v-if="answerGiven" 
			:answer="answer" :answer-status="answerStatus" 
			:is-integer="problemInputType ==='IntegerTypeInput'" :is-multy-integer="problemInputType === 'MultyIntegerTypeInput'" />
		<ResetButton v-if="answerGiven && $config.tournamentMode === 'test'" @resetProblem="resetProblem"></ResetButton>
		<XhrDialog v-if="xhrDialogMode" @close="hideXhrDialog"> {{ xhrDialogContent }} </XhrDialog>
		<ConfirmDialog v-if="confirmDialogMode" :params="confirmDialogParams" @confirmAction="confirmAction"></ConfirmDialog>
	</div>
</template>

<script>
import ProblemResult from './components/ProblemResult.vue'
import HintContainer from './components/HintContainer.vue'
import ResetButton from './components/ResetButton.vue';

export default {
	components: {
		ProblemResult,
		HintContainer,
		ResetButton,
	},

	props: {
		answerStatus: {
			type: Boolean,
			default: false
		},
		answerGiven: {
			type: Boolean,
			default: false
		},
		answer: {
			type: String,
			default: ''
		},
		solution: {
			type: String,
			default: ''
		},
		variant: {
			type: String,
			default: null
		},
		title: {
			type: String,
			default: ''
		},
		cost: {
			type: String,
			default: '0'
		},
		hint: {
			type: Object,
			default() { return {status: true, cost: 1, description: ''} }
		},
		description: {
			type: String,
			default: ''
		},
		image: {
			type: String,
			default: null
		},
		componentPath: {
			type: String,
			default: undefined
		},
		descriptionPath: {
			type: String,
			default: undefined
		},
		problemContent: {
			type: Object,
			default: () => {}
		},
		variantParams: {
			type: Object,
			default: () => {}
		},
		problemInputType: {
			type: String,
			default: 'InteractiveTypeInput'
		},
	},

	data() {
		return {
			newXhr: false,
			xhrDialogMode: false,
			xhrDialogContent: '',
			confirmDialogMode: false,
			confirmDialogParams: {},
			dynamicInput: this.problemInputType ? () => import(`./components/${this.problemInputType}.vue`) : undefined,
			dynamicProblemComponent: () => this.componentPath ? import(`../../../static/problemModules/${this.componentPath}`) : undefined,
			dynamicDescription: this.descriptionPath ? () => import(`../../../static/problemModules/${this.descriptionPath}`) : undefined,
			currentAnswer: '',
			xhrData: undefined,
			confirmActionResult: undefined,
		}
	},

	head() {
		let commonPath = this.componentPath
		if (commonPath) {
			commonPath = commonPath.slice(0, -4)
			return {
				link: [{
					rel: 'stylesheet',
					href: `/problemModules/${commonPath}.css`,
					}
				]
			}
		}
	},
	watch: {
		variantParams(newValue) {
			console.log('variant params changed!', newValue)
		},
		title(newValue) {
			console.log('title changed', newValue)
		},
		currentAnswer(newValue) {
			console.log('update answer!', newValue)
		}
	},

	mounted() {
		console.log(this.problemDescription)
		console.log(this.variantParams)
	},
	
	methods: {
		xhrGet() {
			this.newXhr = false
		},
		showConfirmDialog(params) {
			console.log('show confirm dialog!', params)
			this.confirmDialogMode = true
			this.confirmDialogParams = params
		},
		confirmAction(status) {
			console.log('confirmAction !')
			this.confirmDialogMode = false
			this.confirmActionResult = status
			setTimeout(function(){this.confirmActionResult = undefined}.bind(this), 10)
		},
		showXhrDialog(content) {
			console.log('show xhr dialog')
			this.xhrDialogMode = true
			this.xhrDialogContent = content
		},
		hideXhrDialog() {
			this.xhrDialogMode = false
		},
		async sendAnswer(integerAnswer=false) {
			console.log('send answer!')
			let answer
			if (integerAnswer)
				answer = integerAnswer
			else {
				answer = this.currentAnswer
			}
			let solution
			try {
				solution = this.$refs.problem.innerHTML.replace(/input-save-value/g, 'value')
			}
			catch {
				solution = ''
			}
			await this.$axios.$post('/api/check_answer', {variant: this.variant, answer, solution})
			this.$emit('updateProblemStatus')
		},
		async getHint(){
			const response = await this.$axios.$post('/api/get_hint', {variant: this.variant})
			console.log(response)
			if (response.status) {
				this.$emit('updateHint', response.hint)
				Promise.resolve().then(()=>{  setTimeout(() => { MathJax.typesetPromise();  }, 100);})
			}
		},
		async xhrRequest(xhrParams = {}) {
			const sendUrl = xhrParams.sendUrl ? xhrParams.sendUrl : '/api/xhr'
			const config = xhrParams.config ? xhrParams.config : {'Content-Type': "multipart/form-data"}
			const fileList = xhrParams.xhrFiles ? xhrParams.xhrFiles : []
			let solution
			try {
				solution =  this.$refs.problem.innerHTML.replace(/input-save-value/g, 'value')
			}
			catch {
				solution = ''
			}
			const dataToSend = new FormData()
			dataToSend.append('variant', this.variant)
			dataToSend.append('xhr_params', JSON.stringify(xhrParams))
			for (const xhrFile of fileList) {
				dataToSend.append(xhrFile.title, xhrFile.content)
			}
			console.log(dataToSend)
			dataToSend.append('solution', solution)
			await this.$axios.$post(sendUrl, dataToSend, config)
				.then((resp) => {
					console.log('xhrData: ', resp)
					this.$emit('updateProblemStatus')
					setTimeout(function(){}, 10)
					console.log('params: ', this.variantParams)
					console.log('title: ', this.title)
					this.xhrData = resp
					this.newXhr = true
				})
		},
		updateProblemStatus() {
			console.log('update problem status!')
			this.$emit('updateProblemStatus')
		},
		async resetProblem() {
			await this.$axios.post('/api/reset_problem', {variant: this.variant})
			this.$emit('updateProblemStatus')
		}
	},
}
</script>

<style scoped>

.problem {
	user-select: none;
	-webkit-user-select: none;
}

.problem_solution {
	display: flex;
	pointer-events: none;
	display: inline-flex;
	width: 100%;
	justify-content: center;
	align-items: center;
}

.newTypeProblem {
	margin-top: 50px;
	width: 100%;
	display: inline-flex;
	align-items: center;
	justify-content: center;
}

.problem_container{
	align-self: stretch;
	padding: 40px 60px;
	display: inline-flex;
	flex-direction: column;
	background: #1E8B93;
	border-radius: 20px;
	justify-content: center;
	gap: 40px;
	display: flex;
	color: black;
	font-size: 24px;
	font-family: Montserrat;
	font-weight: 500;
	word-wrap: break-word;
}

.problem_header {
	justify-content: space-between; 
	display: inline-flex;
	align-self: stretch;
	align-items: center;
	
}

.problem_title {
	color: white; 
	font-size: max(25px, min(40px, 2.6vw));
	font-family: Montserrat Alternates; 
	font-weight: 500;
}

.problem_cost {
	padding: 10px 50px;
	text-align: center;
	border-radius: 10px; 
	border: 2px white solid; 
	align-items: center;
	display: inline-flex;
	color: white; 
	font-size: max(15px, min(24px, 1.8vw)); 
	font-family: Montserrat Alternates; 
	font-weight: 500;
	white-space: nowrap;
}

.problem_body {
	align-self: stretch;
	padding: 40px;
	background: white;
	box-shadow: 12px 12px 14px rgba(0, 0, 0, 0.25);
	border-radius: 16px;
	flex-direction: column;
	justify-content: center;
	gap: 20px;
	display: flex;
}

.problem_img{
	max-height: 512px;
	width: 60%;
	display: block;
	margin-left: auto;
	margin-right: auto;
	object-fit: contain;
}

@media(max-width: 800px) {
	.problem {
		margin-top: 10px;
	}
	.problem_container {
		padding: 16px;
		font-size: 12px;
		gap: 10px;
	}
	.problem_cost {
		height: 23px;
		font-size: 12px;
		padding: 4px 10px;
	}
	.problem_name {
		font-size: 14px;
	}
	.problem_body {
		padding: 16px;
	}
	.problem_title {
		font-size: 14px;
	}
}
</style>