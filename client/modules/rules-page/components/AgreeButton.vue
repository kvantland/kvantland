<template>
    <div class="conformation_box">
    <div class="conformation_wrapper">
    <div class="conformation_text">С правилами ознакомился(-лась) и готов(а) приступить!</div>
    <div class="start_button_border">
    <a href="/land">
    <div class ="start_button">
    <div class="start_button_text"> Открыть турнир </div>
    </div>
    </a>
    </div>
    </div>
    </div>
</template>

<script>
export default {
    props: ['rulesDescription']
}
</script>