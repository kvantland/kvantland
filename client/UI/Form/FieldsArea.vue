<template>
    <div class="fieldsArea">
        <slot></slot>
    </div>
</template>

<style>
.fieldsArea {
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
}
</style>