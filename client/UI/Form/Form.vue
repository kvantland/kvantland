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
	box-sizing: border-box;
}
.formBody form {
    display: inline-flex;
    flex-direction: column;
    gap: 20px;
}
.formBackground{
    width: 100%;
    margin-top: 150px;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    display: inline-flex;
	height: 100%;
}
@media (max-width: 800px) {
	.formBody {
		width: 100%;
		gap: 16px;
	}
	.formBackground {
		margin-top: 0px;
	}
}
</style>