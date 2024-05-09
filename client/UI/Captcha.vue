<template>
     <div class="g-recaptcha-outer">
        <div class="g-recaptcha-inner">
            <div class="g-recaptcha" :data-sitekey="sitekey"></div>
        </div>
	 </div>
</template>

<script>
export default {
    data() {
        return {
            sitekey: '6LcWR2MoAAAAABz4UpMRZlmwmWZlvne32dKbc1Kx'
        }
    },
}
</script>

<style>
.g-recaptcha {
	position: relative;
	left: 3px;
	display: inline-flex;
	justify-content: center;
	align-self: center;
}

.g-recaptcha-outer {
	background-color: #F9F9F9;
	border: 1px #99BBFF solid;
	border-radius: 5px;
	width: 320px;
	height: 76px;
	display: inline-flex;
	justify-content: center;
	align-items: center;
}

.g-recaptcha-inner {
	width: 296px;
	height: 70px;
	display: inline-flex;
	justify-content: center;
	align-items: center;
	overflow: hidden;
}
</style>