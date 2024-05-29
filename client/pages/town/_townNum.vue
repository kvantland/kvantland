<template>
    <div class="content_wrapper_town">
        <Breadcrumbs :crumbs="landCrumbs" />
        <svg version="1.1" class="map" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <TownDefs/>
            <image href="/static/map/town-{town}.png" width="1280" height="720"preserveAspectRatio="xMidYMid" clip-path="url(#map_border)" meet />'
            <path stroke="#1E8B93" stroke-width="3px" fill="none" d="
                    M 1.5 21.5
                    v 676
                    a 20 20 0 0 0 20 20
                    h 1237
                    a 20 20 0 0 0 20 -20
                    v -676
                    a 20 20 0 0 0 -20 -20
                    h -1237
                    a 20 20 0 0 0 -20 20
                    z" />

        </svg>
    </div>
</template>
<script>
import TownDefs from "../../modules/town-page/TownDefs.vue"
</script>
<style>
.content_wrapper {
    width: 100%;
    padding: 0 min(5vw, 80px) 80px min(5vw, 80px);
    margin-top: 130px;
    box-sizing: border-box;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    gap: 20px;
    display: inline-flex;
}

svg.map .level {
    text-anchor: middle;
    dominant-baseline: central;
    font-size: 60px;
    font-weight: bold;

    fill: currentColor;
    stroke-width: 2px;
    font-family: Montserrat Alternates
}

svg.map .level-value {
    stroke: inherit;
}

svg.map .level_open:hover {
    color: #ffe488;
    stroke: #9b785c;
}

svg.map .level_open {
    color: #ffc400;
    stroke: #b36d2a;
}

svg.map .level_solved {
    color: #77cc33;
    stroke: #339900;
}

svg.map .level_solved:hover {
    color: #99dd44;
    stroke: #55aa33;
}

svg.map .level_failed {
    color: #dd5533;
    stroke: #993300;
}

svg.map .level_failed:hover {
    color: #ee6644;
    stroke: #aa4433;
}
</style>
