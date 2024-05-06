<template>
    <div class="nav">
        <img class="left_arrow" src="/design/left_arrow.svg" />
        <div class="pages">
            <div v-for="(page, num) in pageAmount" :class="num==selectedNum ? 'selected page': 'page'" :num="num"></div>
        </div>
        <img class="right_arrow" src="/design/right_arrow.svg" />
    </div>
</template>

<script>
export default {
    props: ["pageAmount", "selectedNum"]
}
</script>
