<template>
    <div class="content_wrapper">
        <Breadcrumbs :crumbs="crumbs"/>
        <ProblemContainer :title="title" 
                            :answerStatus="answerStatus"
                            :answerGiven="answerGiven"
                            :answer="answer"
                            :solution="solution"
                            :variant="problemNum"
                            :description="description" 
                            :cost="cost"
                            :image="image"
                            :variantParams="variantParams"
                            :hint="hint"
                            :problemInputType="inputType"
                            :problemComponent="componentType"
                            :problemContent="{problemHTML: problemHTML, problemCSS: problemCSS, problemJS: problemJS}" 
                            @updateHint="updateHint" 
                            @updateProblemStatus="updateProblemStatus"/>
        <SupportInfoContainer />
    </div>
</template>

<script>
import ProblemContainer from "../../modules/problem-page/ProblemContainer/ProblemContainer.vue"
import SupportInfoContainer from "../../modules/problem-page/SupportInfoContaner/SupportInfoContainer.vue"

export default {
    middleware: 'full-auth',
    
    components: {
        ProblemContainer,
        SupportInfoContainer,
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
                    src: '/old-problem-types/confirm_action.js'
                }
            ]
        }
    },

    async asyncData({ params, $axios, redirect }){
        let problemNum = params.problemNum
        let status, problem_data
        let resp = {}
        await $axios.$post("/api/problem_data", {variant: problemNum})
        .then((resp) => {
            status = resp.status
            problem_data = resp.problem
        })
        if (status) {
            for (const prop in problem_data) {
                resp[prop] = problem_data[prop]
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
        resp.variantParams = resp.variantParams
        resp.problemNum = params.problemNum
        console.log(resp)
        return resp
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
	margin-top: 130px;
	box-sizing: border-box;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 40px;
	display: inline-flex;
	padding-bottom: 80px;
	width: 100%;
    padding-left: max(40px, min(5vw, 80px));
    padding-right: max(40px, min(5vw, 80px));
}
</style>