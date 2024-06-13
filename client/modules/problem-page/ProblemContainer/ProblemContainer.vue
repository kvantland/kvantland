<template>
    <div class="problem_container">
        <div class="problem_header">
            <p class="problem_title"> {{ title }} </p>
            <div class="problem_cost"> {{ cost }} </div>
        </div>

        <div class="problem_body">
            <p v-if="description" v-html="description"></p>
            <img v-if="image" class="problem_img" :src="image" />
            <div class="problem newTypeProblem" v-if="problemComponent" ref="problem">
                <component v-if="!answerGiven" :is="dynamicProblemComponent" :xhrData="xhrData" :newXhr="newXhr" 
                    @xhrGet="xhrGet" @showXhrDialog="showXhrDialog" 
                    :problemParams="variantParams" v-model="currentAnswer" @xhrRequest="xhrRequest" @updateProblemStatus="updateProblemStatus"/>
                <div v-if="answerGiven" v-html="solution" class="problem_solution"></div>
            </div>
            <div v-else-if="problemContent" class="problem oldTypeProblem" v-html="problemContent.problemHTML" />
            <HintContainer v-if="hint.description" :description="hint.description" />
        </div>

        <component v-if="!answerGiven" :is="dynamicInput" :hasHint="hint.status" @sendAnswer="sendAnswer" @getHint="getHint"/>
        <ProblemResult v-if="answerGiven" :answer="answer" :answerStatus="answerStatus" :isInteger="problemInputType=='IntegerTypeInput'" />
        <XhrDialog v-if="xhrDialogMode" @close="hideXhrDialog"> {{ xhrDialogContent }} </XhrDialog>
    </div>
</template>

<script>
import ProblemResult from './components/ProblemResult.vue'
import HintContainer from './components/HintContainer.vue'

export default {
    head() {
        return {
            link: [{
                rel: 'stylesheet',
                href: `/problemModules/${this.problemComponent}/${this.problemComponent}.css`,
                }
            ]
        }
    },
    data() {
        return {
            newXhr: false,
            xhrDialogMode: false,
            xhrDialogContent: '',
            dynamicInput: () => import(`./components/${this.problemInputType}.vue`),
            dynamicProblemComponent: () => import(`../../../static/problemModules/${this.problemComponent}/${this.problemComponent}.vue`),
            currentAnswer: '',
            xhrData: undefined,
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
        variantParams: {default: '' },
        problemInputType: {default: 'InteractiveTypeInput'},
    },

    methods: {
        xhrGet() {
            this.newXhr = false
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
                solution = this.$refs['problem'].innerHTML.replace(/input-save-value/g, 'value')
            }
            catch {
                solution = ''
            }
            await this.$axios.$post('/api/check_answer', {variant: this.variant, answer: answer, solution: solution})
            this.$emit('updateProblemStatus')
        },
        async getHint(){
            const response = await this.$axios.$post('/api/get_hint', {variant: this.variant})
            console.log(response)
            if (response.status)
                this.$emit('updateHint', response.hint)
        },
        async xhrRequest(xhrParams) {
            await this.$axios.$post('/api/xhr', {variant: this.variant, xhr_params: xhrParams})
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
        async updateProblemStatus() {
            console.log('update problem status!')
            //this.$emit('updateProblemStatus')
        }
    },

    mounted() {
        console.log(this.variantParams)
    },
    wath: {
        variantParams(newValue) {
            console.log('variant params changed!', newValue)
        },
        title(newValue) {
            console.log('title changed', newValue)
        }
    }
}
</script>

<style scoped>
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