<template>
    <a class="contact_button" :href="contactInfo.source_link" target="_blank">
        <img class="contact_icon" loading="lazy" :src="`/icons/${contactInfo.image}`" />
    </a>
</template>

<script>
export default {
    props: ["contactInfo"]
}
</script>

<style>
</style>