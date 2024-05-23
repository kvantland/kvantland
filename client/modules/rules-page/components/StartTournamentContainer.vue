<template>
<div class="conformation_box">
    <div class="conformation_wrapper">
        <p class="conformation_text">С правилами ознакомился(-лась) и готов(а) приступить!</p>
        <div class="start_button_border">
            <NuxtLink  to="/land" target="_blank">
                <div class ="start_button"> Открыть турнир </div>
            </NuxtLink>
        </div>
    </div>
</div>
</template>
<style scoped>
.conformation_box {
    align-self: stretch;
    padding-left: 40px;
    padding-right: 40px;
    padding-top: 30px;
    padding-bottom: 30px;
    background: #1E8B93;
    border-radius: 20px;
    flex-direction: column;
    justify-content: center;
    align-items: flex-end;
    gap: 10px;
    display: flex;
}

.conformation_text {
    font-weight: 600;
}

.conformation_wrapper {
    align-self: stretch;
    justify-content: space-between;
    align-items: center;
    display: inline-flex;
}

.conformation_text {
    white-space: nowrap;
    color: white;
    font-size: max(15px, min(20px, 1.5vw));
}
.start_button_border {
    align-self: stretch;
    justify-content: flex-start;
    align-items: flex-start;
    display: flex;
}
.start_button {
    margin-left: 10px;
    white-space: nowrap;
    flex: 1 1 0;
    height: 30px;
    padding: 10px min(80px, 5vw);
    background: linear-gradient(180deg, #FCFCFC 16%, white 20%, #FFFFFF 55%, #EFEFEF 80%);
    box-shadow: 7px 7px 6.699999809265137px #1A5866;
    border-radius: 10px;
    overflow: hidden;
    justify-content: center;
    align-items: center;
    gap: 10px;
    display: flex;
    text-align: center;
    color: black;
    font-size: max(17px, min(24px, 1.8vw));
}
</style>