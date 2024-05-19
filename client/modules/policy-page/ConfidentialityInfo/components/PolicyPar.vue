<template>
    <div class="par">
        <p class="header">{{ num + 1 }}. {{ parHeader }}</p>
        <div class="content">
            <p v-for="(item, index) in parDescription"> {{ index + 1 }}.
                <span class="description" v-html="item" />
            </p>
        </div>
	</div>
</template>

<script>
export default {
    props: ['parHeader', 'parDescription', 'num']
}
</script>
<style>
.par {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.par .header {
    color: black;
    text-transform: none;
    font-family: Montserrat;
    font-size: 20px;
    font-weight: 600;
}

.par .content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 20px;
    font-weight: 400;
}
</style>