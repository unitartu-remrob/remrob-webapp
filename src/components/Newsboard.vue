<template>
	<vue-simple-scrollbar v-html="content">
		
	</vue-simple-scrollbar>
</template>

<script>
import VueSimpleScrollbar from 'vue-simple-scrollbar'
export default {
	name: 'Newsboard',
	components: {
		VueSimpleScrollbar
	},
	props: {
		content: {
			type: String,
			default: ""
		}
	},
	data: function() {
		return {
			
		}
	},
	methods: {

	},
	created: function() {

	},
}
</script>

<style>
@import '~vue-simple-scrollbar/dist/vue-simple-scrollbar.css';

.remrob-info .card-body {
	/* display: flex; */
	/* justify-content: center; */
	font-size: 1.2rem;
	line-height: 1.2rem;
	overflow: auto;
	overflow-x: hidden;
	padding: 1.5rem 2rem;
}

</style>