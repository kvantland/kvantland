<template>
    <Form>
        <AccFormViewMode v-if="mode=='view'" @changeToEditMode="changeToEditMode" />
        <AccFormEditMode v-else-if="mode=='edit'" />
    </Form>
</template>

<script>
import AccFormViewMode from "../modules/acc-page/AccFormViewMode/AccFormViewMode.vue"
import AccFormEditMode from "../modules/acc-page/AccFormEditMode/AccFormEditMode.vue"

export default {
    layout: 'forms',
    
    data() {
        return {
            'mode': 'view',
        }
    },

    components: {
        AccFormEditMode,
        AccFormViewMode,
    },

    methods: {
        changeToEditMode() {
            console.log('change mode!')
            this.mode = 'edit'
        }
    }
}
</script>