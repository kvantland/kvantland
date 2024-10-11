<template>
<nav class="breadcrumbs">
    <template v-for="(item, num) in crumbs">
        <NuxtLink :key="`crumb_${num}`" :to="item.link"> {{ item.name }} </NuxtLink>
        <div :key="`between_arrows_${num}`" class="between">
            <img src="/icons/breadcrumbs.svg" />
            <img src="/icons/breadcrumbs.svg" />
        </div>
    </template>
</nav>
</template>

<script>
export default {
    props: ["crumbs"]
}
</script>
<style scoped>
nav.breadcrumbs {
    white-space: nowrap;
    justify-content: flex-start; 
    align-items: center; 
    gap: min(20px, 1.5vw); 
    display: inline-flex;
    color: #1E8B93; 
    font-size: max(30px, min(3.1vw, 40px)); 
    font-family: Montserrat Alternates; 
    font-weight: 500;
}

.between {
    display: inline-flex;
}

.between img {
    max-width: 16.8px;
    height: max(15px, min(1.8vw, 24px)); 
}

@media(max-width: 800px) {
	nav.breadcrumbs {
		font-size: 14px;
	}
	.between img {
		height: 8px;
	}
}
</style>