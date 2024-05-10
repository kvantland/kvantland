<template>
    <div class="formBackground">
        <div class="formBody">
            <slot />
        </div>
    </div>
</template>

<style>
.formBody {
    -webkit-user-select: none;
    user-select: none;
    display: inline-flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px;
    gap: 21px;
    background: white;
    box-shadow: -4px -4px 10px rgba(0, 0, 0, 0.10);
    border-radius: 20px;
    align-items: stretch;
    margin: 0 auto;
    margin-bottom: 100px;
}
.formBody form {
    display: inline-flex;
    flex-direction: column;
    gap: 20px;
}
.formBackground{
    width: 100%;
    margin-top: 80px;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    display: inline-flex;
}
</style>