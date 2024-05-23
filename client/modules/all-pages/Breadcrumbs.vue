<template>
<nav class="breadcrumbs">
    <template v-for="item in crumbs">
        <NuxtLink :to="item.link"> {{ item.name }} </NuxtLink>
        <div class="between">
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
</style>