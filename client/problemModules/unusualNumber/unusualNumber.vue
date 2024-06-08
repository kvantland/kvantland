<template>
	<div class="plot_area">
		<div class="flex_box">
		<div class="row">
			<div class="field" v-for='index in in_row' :key="index">
				<input class="fieldInput" :ref="'textInput' + index" type="text" min="0" max="9" maxlength="1" value="" @keypress="handleKeyPress(index, $event)" @keyup="handleKeyUp(index, $event)">
			</div>
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
    	let ans = Array(in_row)
        return {
			in_row: in_row,
			ans: ans
        }
    },

    methods: {
    	handleKeyPress(index, event) {
    		if (event.key.length === 1 && /\D/.test(event.key)) {
        		event.preventDefault();
     		}

      		const maxLength = this.$refs['textInput' + index][0].maxLength;
      
	      	if (maxLength !== null && maxLength !== -1) {
	        	const length = this.$refs['textInput' + index][0].value.trim().length;
	        	if (length + 1 > parseInt(maxLength)) {
	          		event.preventDefault();
	        	}
	      	}
	    },
        handleKeyUp(index, event) {
      		this.$refs['textInput' + index][0].setAttribute('value', event.target.value);
      		this.$set(this.ans, index, event.target.value);
      		this.$emit('updateAnswer', parseInt(this.ans.join('')));
    	}
    },
}
</script>
<style>
.plot_area {
	margin-top: 20px;
	display: flex;
	justify-content: center;
}

.flex_box{
	display: inline-flex;
	flex-direction: column;
	border: 1px solid;
}

.row{
	display: flex;
	flex-direction: row;
	height: max(60px, min(8vw, 96px));;
}

.field {
	display: flex;
	font-family: Montserrat Alternates;
	font-weight: 600; 
	font-size:64px;
	border:1px black solid;
	justify-content: center;
	text-align: center;
	width: max(60px, min(8vw, 96px));
	align-items: center;
}

.fieldInput {
	font-family: Montserrat Alternates;
	font-weight: 400;
	font-size:64px;
	stroke: black;
	display: block;
    margin:auto;
    width: 80%;
    height: 80%;
    text-align: center;
    background: none;
}

.fieldinput:focus{
	outline: none;
}
</style>