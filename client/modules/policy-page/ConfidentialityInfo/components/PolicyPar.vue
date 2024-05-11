<template>
    <div class="par">
        <div class="header" v-html="parHeader"></div>
        <div class="content" v-html="parDescription"> </div>
	</div>
</template>

<script>
export default {
    props: ['parHeader', 'parDescription']
}
</script>