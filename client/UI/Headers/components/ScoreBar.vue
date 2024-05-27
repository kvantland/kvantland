<template>
    <div class="score_bar">
        <p> {{ login }} </p>
        <p> Счёт: {{ score }} </p>
    </div>
</template>

<script>
    export default {
        data({$auth}) {
            return {
                login: $auth.user.name,
                score: $auth.user.score
            }
        }
    }
</script>

<style scoped>
.score_bar {
    padding: 10px min(40px, 2.6vw);
	box-shadow: 0px 2px 14.800000190734863px rgba(0, 0, 0, 0.20); 
	border-radius: 10px; 
	border: 3px #1E8B93 solid; 
	justify-content: flex-start; 
	align-items: center; 
	gap: min(40px, 2.6vw); 
	display: flex;
    font-family: Montserrat Alternates;
    font-size: 20px;
    font-weight: 500;
}
</style>