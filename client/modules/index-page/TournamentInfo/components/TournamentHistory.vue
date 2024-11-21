<template>
    <div class="history">
        <div class="content">
            <div v-for="(historyItem, num) in tournamentHistory" :key="`history_item_${num}`" class="item">
                <div class="text_cont">
                    <div class="header"> {{historyItem['event_date']}} </div>
                    <div class="text"> {{historyItem['event_name']}} </div>
                </div>
                <div class="rect"></div>
            </div>
        </div>
        <hr size="2" noshade="" color="white">
    </div>
</template>

<script>
export default {
    props: ['tournamentHistory']
};
</script>

<style scoped>
.history {
    width: 100%;
	display: inline-flex;
	flex-direction: column;
}

.history .content {
	display: inline-flex;
	justify-content: space-between;
}

.history hr {
	position: relative;
	top: -21px;
	color: white;
}

.history .content .item {
	display: inline-flex;
	flex-direction: column;
	gap: 30px;
}

.history .content .item .rect {
	width: 40px;
	height: 40px;
	background-color: white;
	border-radius: 10px;
}

.history .content .item .text_cont {
	display: inline-flex;
	flex-direction: column;
	gap: 20px;

}

.history .content .item .text_cont .header {
	color: white;
	font-size: max(2vw, min(32px, 2.5vw));
	font-family: Montserrat Alternates;
	font-weight: 600;
}

.history .content .item .text_cont .text {
	color: white;
	font-size: max(15px, min(24px, 1.8vw));
	font-family: Montserrat;
	font-weight: 400;
}

@media(max-width: 800px) {
	.history .content .item .text_cont {
		gap: 8px;
	}
	.history .content .item .text_cont .header {
		font-size: 2.2vw;
	}
	.history .content .item .text_cont .text {
		font-size: 2.3vw;
	}
	.history .content .item .rect {
		width: 20px;
		height: 20px;
		border-radius: 5px;
	}
	.history hr {
		top: -11px;
	}
	.history .content .item {
		gap: 8px;
	}
}
</style>
