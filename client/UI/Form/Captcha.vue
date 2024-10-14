<template>    
    <div class="captcha_with_error">
        <div class="g-recaptcha-outer">
            <div class="g-recaptcha-inner">
                <recaptcha class="recaptcha"/>
            </div>
        </div>
        <div class="error_container" v-if="error">
            <img class="captcha_error" src="/icons/info.svg" />
            <p class="captcha_error"> {{ error }} </p>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        error: {default:""},
    }
}
</script>

<style scoped>
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

.captcha_with_error {
    display: inline-flex;
    flex-direction: column;
    gap: 6px;
}

.error_container {
    display: inline-flex;
    gap: 6px;
    align-self: flex-start;
    padding-left: 20px;
}

img.captcha_error {
    align-self: center;
	width: 16px;
	height: 16px;
}

p.captcha_error{
	color: #B62C5A;
	font-size: 12px;
	font-weight: 600;
}
</style>