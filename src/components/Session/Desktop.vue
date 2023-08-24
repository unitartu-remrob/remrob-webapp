<template>
	<div class="resp-container" :style="`background-image: url(${require('@/assets/monitor-icon.svg')})`">
		<iframe
			v-if="started"
			:src="source"
			class="resp-iframe"
			:style="`display: ${preventScroll}`"
		></iframe>
	</div>
</template>

<script>
export default {
	props: ['source', 'started'],
	data() {
		return {
			loaded: false
		}
	},
	computed: {
		preventScroll() {
			return this.loaded ? 'block' : 'none'; // doesn't woooork
		}
	},
	mounted() {
		this.loaded = true;
	}
}
</script>

<style scoped>
.resp-container {
    position: relative;
    overflow: hidden;
    padding-top: 56.25%;
    background-size: 100% 100%;
    background-repeat: no-repeat;
	transform: skew(0, 16deg);
}
.resp-iframe {
    position: absolute;
    top: -6rem;
    left: 0;
    width: 100%;
    height: 100%;
	padding: 0.5rem 1.5rem 0;
	transform: scale(0.74);
	background-color: #000;
    border: 0;
	box-shadow: 0px 180px 80px -50px rgba(0,0,0,0.69);
	display: none;
}
</style>