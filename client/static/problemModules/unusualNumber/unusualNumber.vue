<template>
	<div class="flex_box">
		<div class="row">
			<div class="field" v-for='index in in_row' :key="index">
				<input :class="`fieldInput ${index}`" v-model="ans[index]" type="text" min="0" max="9" :maxlength="maxLength" value="" @keypress="handleKeyPress(index, $event)" @keyup="handleKeyUp(index, $event)">
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
    	const in_row = 5
    	const maxLength = 1
    	let ans = Array.from({ length: in_row + 1 }, () => '');
        return {
			in_row: in_row,
			ans: ans,
			maxLength: maxLength,
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
        handleKeyUp(index, event) {
        	console.log(this.ans, index)
      		this.$emit('updateAnswer', parseInt(this.ans.join('')));
    	}
    },
}
</script>
