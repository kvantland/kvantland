<template>
    <div class="hint_wrapper">
        <div class="header">
            <img class="hint_icon" src="/icons/hint_icon.svg" />
            <p class="title">Подсказка</p>
        </div>
        <p class="description">{{ description }}</p>
    </div>
</template>

<script>
export default {
    props: {
        description: {default: ''}
    }
}
</script>

<style scoped>
.hint_wrapper {
	padding: 40px;
	background: white;
	border-radius: 20px;
	border: 3px #1E8B93 solid;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 20px;
	display: inline-flex;
	align-self: stretch;
}

 .header {
	align-self: flex-start;
	justify-content: flex-end;
	align-items: center;
	gap: 20px;
	display: inline-flex;
}

.header .title {
	font-size: 24px;
	font-family: Montserrat;
	font-weight: 600;
}

.description {
    align-self: flex-start;
	font-size: 20px;
	font-family: Montserrat;
	font-weight: 500;
}
@media(max-width: 800px) {
	.hint_wrapper {
		border-radius: 8px;
		padding: 16px;
		gap: 10px;
	}
	.description {
		font-size: 12px;
	}
	.header .title {
		font-size: 12px;
	}
	.header {
		gap: 5px;
	}
	.hint_icon {
		height: 18px;
	}
}
</style>