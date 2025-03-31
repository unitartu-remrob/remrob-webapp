<template>
    <div class="error">
        <h1 class="display-2">404 Error</h1>
        <p>The resource could not be found.</p>
        <router-link to="/home" exact>
            Go to home page
        </router-link>
    </div>
</template>

<script>
export default {

}
</script>

<style>
	.error {
		display: flex;
		width: 100%;
		height: 100%;
		flex-direction: column;
		align-items: center;
		margin-top: 15rem;
		font-size: 2rem;
	}
</style>