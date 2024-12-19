<template>
    <div class="number-section">
        <span v-for="(number, index) in data[side]" :key="`number-${data.id}-${index}`" class="number">
            {{ number }}
            <span v-if="index < data[side].length - 1">
                <div :class="dropZoneClass(index)" @dragover.prevent="handleDragOver(index)" @drop="handleDrop(index)">
                    <div 
                        v-if="hasSign(index)" :class="signClass(getSign(index))" draggable
                        @dragstart="handleDragStart(index)" @dragend="handleDragEnd">
                        {{ getSign(index) }}
                    </div>
                </div>
            </span>
        </span>
    </div>
</template>


<script>

export default {
    props: {
        data: { type: Object, required: true },
        signs: { type: Array, required: true },
        side: { type: String, required: true },
        currentDropIndex: { type: Number, default: null }
    },

    methods: {
        handleDragStart(index) {
            this.$emit('dragstart', this.getAdjustedIndex(index));
        },

        handleDragEnd() {
            this.$emit('dragend');
        },

        handleDragOver(index) {
            this.$emit('dragover', this.getAdjustedIndex(index));
        },

        handleDrop(index) {
            this.$emit('drop', this.getAdjustedIndex(index));
            this.handleDragEnd(); // Вызов dragend здесь
        },

        getAdjustedIndex(index) {
            return this.side === 'right' ? index + this.data.left.length -1: index;
        },

        getSign(index) {
            return this.signs[this.getAdjustedIndex(index)];
        },

        hasSign(index) {
            return !!this.signs[this.getAdjustedIndex(index)];
        },

        dropZoneClass(index) {
            const adjustedIndex = this.getAdjustedIndex(index);
            return {
                'drop-zone': true,
                'fill': this.hasSign(index),
                'highlight': this.currentDropIndex === adjustedIndex
            };
        },

        signClass(sign) {
            return {
                'sign': true,
                'red': sign === '+',
                'violet': sign === '−',
                'orange': sign === '×'
            };
        }
    }
};
</script>
