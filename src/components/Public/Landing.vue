<template>
    <div class="landing-container">
        <div class="landing">
            <RemrobIntro/>
            <PublicContainers />
        </div>
    </div>
</template>

<script>
import RemrobIntro from './RemrobIntro.vue';
import PublicContainers from './Containers.vue';

export default {
    name: 'Landing',
    components: {
        RemrobIntro,
        PublicContainers,
    },
    data() {
        return {

        }
    },
    created() {

    },
}
</script>

<style>
.text-ubuntu-500 {
    font-family: "Ubuntu", sans-serif;
	font-weight: 500;
	font-style: normal;
}

.text-ubuntu-600 {
    font-family: "Ubuntu", sans-serif;
	font-weight: 600;
	font-style: normal;
}

.text-arvo-400 {
    font-family: "Arvo", sans-serif;
    font-weight: 400;
    font-style: normal;
}

.landing-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgb(217,233,212);
    background: linear-gradient(215deg, rgba(217,233,212,1) 7%, rgba(217,233,212,1) 12%, rgba(133,135,152,1) 38%, rgba(31,77,89,0.8914900957527807) 55%, rgba(46,71,93,0.9705861409505209) 70%);
}
.landing {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2%;
    margin-top: 4rem;
    height: 90vh;
}
</style>