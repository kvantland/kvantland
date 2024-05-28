<template>
    <div class="problem_container">
        <div class="problem_header">
            <p class="problem_title"> {{ title }} </p>
            <div class="problem_cost"> {{ cost }} </div>
        </div>

        <div class="problem_body">
            <p v-if="description" v-html="description"></p>
            <img v-if="image" class="problem_img" :src="image" />
            <div class="newTypeProblem" v-if="problemComponent">
                <component :is="dynamicProblemComponent" />
            </div>
            <div v-if="problemContent" class="oldTypeProblem" v-html="problemContent.problemHTML" />
            <HintContainer v-if="hint.description" :description="hint.description" />
        </div>

        <component v-if="!answerGiven" :is="dynamicInput" :hasHint="hint.status" @sendAnswer="sendAnswer" @getHint="getHint"/>
        <ProblemResult v-if="answerGiven && problemInputType=='IntegerTypeInput'" :answer="answer" :answerStatus="answerStatus" />
    </div>
</template>

<script>
import ProblemResult from './components/ProblemResult.vue'
import HintContainer from './components/HintContainer.vue'

export default {
    data() {
        return {
            dynamicInput: () => import(`./components/${this.problemInputType}.vue`),
            dynamicProblemComponent: () => import(`../../../problemModules/${this.problemComponent}.vue`)
        }
    },

    components: {
        ProblemResult,
        HintContainer,
    },

    props: {
        answerStatus: {default: false},
        answerGiven: {default: false},
        answer: {default: ''},
        solution: {default: ''},
        variant: {default: null},
        title: {default: ''},
        cost: {default: 0},
        hint: {default: null },
        description: {default: ''},
        image: {default: null},
        problemComponent: {default: null},
        problemContent: {default: null},
        variantParams: {default: null},
        problemInputType: {default: 'InteractiveTypeInput'}
    },

    methods: {
        async sendAnswer(answer) {
            await this.$axios.$post('/api/check_answer', {variant: this.variant, answer: answer})
            window.location.reload('true')
        },
        async getHint(){
            const response = await this.$axios.$post('/api/get_hint', {variant: this.variant})
            console.log(response)
            if (response.status)
                this.$emit('updateHint', response.hint)
        }
    },
}
</script>

<style scoped>
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
    width: 100%;
    display: block;
    margin-left: auto;
    margin-right: auto;
    object-fit: contain;
}
</style>