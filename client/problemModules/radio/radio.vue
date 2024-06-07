<template>
    <div class="left_area">
        <div class="answer_list">
            <label v-for="(answer, k) in answers" :key="`label_${k}`">
                <input v-if="choosed != k" name="answer" type="radio" required :value="k" @input="chooseAnswer(k)" />
                <input v-else name="answer" type="radio" required :value="k" @input="chooseAnswer(k)" checked />
                {{ answer  }}
            </label>
        </div>
    </div>
</template>

<script>
export default {
    props: ['problemParams'],
    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },
    data() {
        return {
            answers: this.problemParams.answers,
            choosed: undefined,
        }
    },
    methods: {
        chooseAnswer(k) {
            console.log(k)
            this.choosed = k
            this.$emit('updateAnswer', k)
        }
    }
}
</script>

<style scoped>
.left_area {
    display: inline-flex;
    width: 100%;
    align-items: flex-start;
}

.answer_list {
    display: inline-flex;
    flex-direction: column;
}

label {
    display: flex;
    gap: 10px;
    align-items: center;
}
</style>