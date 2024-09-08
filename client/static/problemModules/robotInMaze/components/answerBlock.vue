<template>
    <div 
        :class="['block', blockData.type, blockData.select ? 'select' : 'not_select']" 
        :block_id="blockData.id"  @mousedown="moveFromAnswerArea(blockData.id, $event)" 
		@touchstart="moveFromAnswerArea(blockData.id, $event.touches[0])"> 
		<p>{{ blockData.text }} </p>
		<div v-if="blockData.type === 'cycle'" class="insert_zone">
            <answerBlock v-for="block in blockData.children" :key="`answer_block_${block.id}`" 
                @updateAnswerArea="updateAnswerArea" @updateTargetBlock="updateTargetBlock"
                :blockData="block" :answerAreaBlocks="answerAreaBlocks" 
                :targetBlock="targetBlock"></answerBlock>
        </div>
    </div>
</template>

<script>
import answerBlock from './answerBlock.vue';

export default {
    name: 'answerBlock',

    components: {answerBlock},

    props: {
        blockData: {
            type: Object,
            default() {return {}},
        },
        answerAreaBlocks: {
            type: Array,
            default() {return []}
        },
        targetBlock: {
            type: Object,
            default() {return undefined}
        }
    },

    methods: {
        findTarget(blockNum, level=this.answerAreaBlocks) {
			const newLevelBlocks = []
			for (const block of level) {
				const newBlock = JSON.parse(JSON.stringify(block))
				if (block.id.toString() === blockNum.toString()) {
					this.$emit('updateTargetBlock', newBlock)
				}
				else {
					if (block.children) {
						newBlock.children = this.findTarget(blockNum, block.children)
					}
					newLevelBlocks.push(newBlock)
				}
			}
			return newLevelBlocks
		},

		moveFromAnswerArea(blockNum, event) {

			if (this.targetBlock) {
				return
			}
            const newAnswerArea = this.findTarget(blockNum)
			this.$emit('updateAnswerArea', newAnswerArea)
			this.$emit('updateAnswer', this.answerAreaBlocks)
			this.$emit('startDrag', event)
		},

        updateAnswerArea(newAnswerArea) {
            this.$emit('updateAnswerArea', newAnswerArea)
        },

        updateTargetBlock(newBlock) {
            this.$emit('updateTargetBlock', newBlock)
            this.$emit('startDrag', event)
        }
    }
}
</script>