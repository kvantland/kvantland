<template>
	<div class="flex_box">
		<div class="row">
			<div class="field" v-for='index in inRow' :key="`field_${index}`">
				<input :class="`fieldInput_${index}`" v-model="ans[index]" type="text"
                    min="0" max="9" :maxlength="maxLength" :input-save-value="ans[index]" @keypress="handleKeyPress(index, $event)" 
                    @keyup="handleKeyUp(index)">
			</div>
		</div>
	</div>  
</template>

<script>
export default {
    props: ["problemParams"],
    model: {
        prop: 'answer',
        event: 'updateAnswer'
    },
    data() {
        return {
			inRow: this.problemParams.fieldsAmount,
			ans:  Array.from({ length: this.problemParams.fieldsAmount + 1 }, () => ''),
			maxLength: 1,
        }
    },

    methods: {
    	handleKeyPress(index, event) {
    		if (event.key.length === 1 && /\D/.test(event.key)) {
        		event.preventDefault();
     		}

      		const maxLength = this.maxLength
	      	if (maxLength !== null && maxLength !== -1) {
	        	const length = this.ans[index].trim().length;
	        	if (length + 1 > parseInt(maxLength)) {
	          		event.preventDefault();
	        	}
	      	}
	    },
        handleKeyUp(index) {
      		this.$emit('updateAnswer', parseInt(this.ans.join('')));
    	}
    },
}
</script>
