<template>
    <div class="content_wrapper">
        <ConfidentialityInfo />
    </div>
</template>


<script>
import ConfidentialityInfo from '../../modules/policy-page/ConfidentialityInfo/ConfidentialityInfo.vue'
    export default {

        components: {
            ConfidentialityInfo,
        },
        head() {
            return {
                title: 'Квантландия'
            };
        },
    };
</script>

<style scoped>
.content_wrapper {
    width: 100%;
	padding-bottom: 80px;
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
@media(max-width: 800px) {
	.content_wrapper {
		margin-top: 0px;
		padding: 0px;
		font-size: 12px;
	}
}
</style>
