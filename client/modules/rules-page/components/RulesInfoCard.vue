<template>
    <div class="span_wrapper">
        <span class="span_text" v-html="rulesDescription"> </span>
    </div>
</template>

<script>
export default {
    props: ['rulesDescription']
}
</script>