<template>
    <div class="content_box">
        <img class="icon" loading="lazy" :src="`/icons/${cardImage}`" />
        <p v-html="cardDescription"></p>
	</div>
</template>

<script>
export default {
    props: ['cardImage', 'cardDescription']
}
</script>