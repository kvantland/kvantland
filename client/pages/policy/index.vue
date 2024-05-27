<template>
    <div class="content_wrapper">
        <ConfidentialityInfo />
    </div>
</template>


<script>
import ConfidentialityInfo from '../../modules/policy-page/ConfidentialityInfo/ConfidentialityInfo.vue'
    export default {
        head() {
            return {
                title: 'Квантландия'
            };
        },

        components: {
            ConfidentialityInfo,
        },
    };
</script>

<style>
.content_wrapper {
    width: 100%;
    padding: 0 80px 80px 80px;
    margin-top: 130px;
    box-sizing: border-box;
    flex-direction: column;
    justify-content: center;
    display: inline-flex;
}

.content_wrapper * {
    font-family: Montserrat;
    word-wrap: break-word;
    text-align: justify;
}
</style>
