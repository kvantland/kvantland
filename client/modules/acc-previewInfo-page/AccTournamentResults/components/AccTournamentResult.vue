<template>
    <div class="tournament_result" num="{tournament_amount - tournament}">
        <img class="win_cup" src="/icons/win_cup.svg" />
        <div class="text_content">
            <p class="tournament_number"> {{ title }} </p>
            <p class="score"> {{ score }} </p>
        </div>
    </div>
</template>

<script>
export default {
    props: ['title', 'score'],
}
</script>

<style>
.tournament_result {
	display: flex;
	flex-direction: row;
	align-self: stretch;
	gap: 15px;
	padding: 10px 20px;
	border-radius: 6px;
	background: rgba(26, 88, 102, 0.1);
	font-size: 12px;
}

.tournament_result .text_content {
	display: flex;
	flex-direction: column;
	gap: 8px;
	align-self: center;
}

.tournament_result .tournament_number {
	font-weight: 600;
}

.tournament_result .score {
	font-weight: 500;
}
</style>