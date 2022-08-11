<template>
	<div class="resp-container" :style="`background-image: url(${require('../assets/screen-icon.svg')})`">
		<iframe
			:src="source"
			class="resp-iframe"
		></iframe>
	</div>
</template>

<script>
export default {
	props: ['source'],
}
</script>

<style scoped>
.resp-container {
    position: relative;
    overflow: hidden;
    padding-top: 56.25%;
    background-size: 100% 100%;
    background-repeat: no-repeat;
}
.resp-iframe {
    position: absolute;
    top: -3.5rem;
    left: 0;
    width: 100%;
    height: 100%;
	padding: 0.5rem 1.5rem 0;
	transform: scale(0.81);
	background-color: #000;
    border: 0;
	box-shadow: 3px 87px 57px -34px rgba(0,0,0,0.69);
}
</style>