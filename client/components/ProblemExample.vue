<template>
    <div class="problem" :num="`${num}`">
        <div class="head">
            <div class="name"> {{ problemInfo.title }} </div>
            <div class="cost"> {{ problemInfo.cost }} </div>
        </div>

        <div class="body">
            <div class="text_container">
                <p v-html="problemInfo.desc"></p>
            </div>
            <img class="image" loading="lazy" :src="`/design/problem_img/${problemInfo.image}`" />
        </div>

        <div class="button_area">
            <div class="button answer"> Посмотреть ответ </div>
            <div class="button solution"> Посмотреть решение </div>
	    </div>
	 </div>
</template>

<script>
export default {
    props: ["problemInfo", "num"],
};
</script>