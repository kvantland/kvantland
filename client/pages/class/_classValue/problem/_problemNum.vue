<template>
		<div class="content_wrapper">
			<Breadcrumbs :crumbs="crumbs"/>
			<ProblemContainer 
				:title="title" 
				:answer-status="answerStatus"
				:answer-given="answerGiven"
				:answer="answer"
				:solution="solution"
				:variant="problemNum"
				:class-value="classValue"
				:description="description" 
				:cost="cost"
				:image="image"
				:variant-params="variantParams"
				:hint="hint"
				:problem-input-type="inputType"
				:component-path="componentPath"
				:description-path="descriptionPath"
				:problem-content="{problemHTML: problemHTML, problemCSS: problemCSS, problemJS: problemJS}" 
				@updateHint="updateHint" 
				@updateProblemStatus="updateProblemStatus"/>
			<SupportInfoContainer />
		</div>
</template>



<script>
import ProblemContainer from "~/modules/problem-page/ProblemContainer/ProblemContainer.vue";
import SupportInfoContainer from "~/modules/problem-page/SupportInfoContaner/SupportInfoContainer.vue";

export default {
	components: {
		ProblemContainer,
		SupportInfoContainer,
	},

	middleware: 'full-auth',

	async asyncData({ params, $axios, redirect }){
		const problemNum = params.problemNum
		const classValue = params.classValue
		let status, problemData
		const resp = {}
		await $axios.$post("/api/problem_data", {variant: problemNum})
		.then((resp) => {
			status = resp.status
			problemData = resp.problem
		})
		if (status) {
			for (const prop in problemData) {
				resp[prop] = problemData[prop]
			}
		}
		else {
			return redirect('/')
		}
		await $axios.$post('/api/problem_breadcrumbs', {variant: params.problemNum})
		.then((res) => {
			if (res.status)
				resp.crumbs = res.breadcrumbs
			else
				resp.crumbs = []
		})
		resp.problemNum = params.problemNum
		resp.classValue = classValue

		console.log(resp)
		return resp
	},

	head() {
		return {
			link: [
				{ 
					rel: 'stylesheet', 
					href: `${this.problemCSS}`
				}
			],
			script: [
				{
					body: true,
					src: `${this.problemJS}`,
					type: 'text/ecmascript',
				},
				{
					body: true,
					src: '/old-problem-types/confirm_action.js',
				},
				{
					body: true,
					defer: true,
					innerHTML:  "Promise.resolve().then(()=>{ setTimeout(() => {    MathJax.typesetPromise();  }, 100);})",
				}
			],
		}
	},

	methods: {
		updateHint(hint) {
			console.log(hint)
			this.$set(this.hint, 'description', hint)
			this.$set(this.hint, 'status', false)
			this.$auth.fetchUser()
		},
		async updateProblemStatus() {
			console.log('update_req')
			let status, problemData
			await this.$axios.$post("/api/problem_data", {variant: this.problemNum})
			.then((resp) => {
				status = resp.status
				problemData = resp.problem
				this.$auth.fetchUser()
			})
			if (status) {
				this.cost = problemData.cost
				this.variantParams = problemData.variantParams
				this.answerStatus = problemData.answerStatus
				this.answerGiven = problemData.answerGiven
				this.answer = problemData.answer
				this.solution = problemData.solution
			}
		}
	},
}
</script>

<style scoped>
.content_wrapper{
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 40px;
	display: inline-flex;
	padding-bottom: 80px;
	width: 100%;
}
@media(max-width: 800px) {
	.content_wrapper {
		margin-top: 0px;
		gap: 10px;
		padding: 0px;
	}
}
</style>