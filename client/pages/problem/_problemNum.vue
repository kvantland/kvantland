<template>
    <div class="content_wrapper">
        <Breadcrumbs :crumbs="crumbs"/>
        <ProblemContainer :title="title" 
                            :description="description" 
                            :cost="cost"
                            :image="image"
                            :variantParams="variantParams"
                            :hint="hint"
                            :problemInputType="inputType"
                            :problemComponent="problemComponent"
                            :problemContent="{problemHTML: problemHTML, problemCSS: problemCSS, problemJS: problemJS}" />
        <SupportInfoContainer />
    </div>
</template>

<script>
import ProblemContainer from "../../modules/problem-page/ProblemContainer/ProblemContainer.vue"
import SupportInfoContainer from "../../modules/problem-page/SupportInfoContaner/SupportInfoContainer.vue"

export default {
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
                    src: '/problem-types/confirm_action.js'
                }
            ]
        }
    },

    async asyncData({ params, $axios }){
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
        await $axios.$post('/api/problem_breadcrumbs', {variant: params.problemNum})
        .then((res) => {
            if (res.status)
                resp.crumbs = res.breadcrumbs
            else
                resp.crumbs = []
        })
        console.log(resp)
        return resp
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