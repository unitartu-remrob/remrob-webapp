<template>
    <b-container fluid>
        <b-row class="m-2">
            <b-col>
                <b-card style="max-width: 30vw" img-fluid class="text-center" :img-src="require('../assets/calendar.png')" title="Book a slot">
                    <b-card-text>Book a robot or a container</b-card-text>
                    <b-button @click="$router.push({name: 'Booking'})">Go to booking</b-button>
                </b-card>
            </b-col>
        </b-row>
        <canvas id='canvas'>h264Preview_01_main</canvas>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { loadPlayer } from 'rtsp-relay/browser';
export default {
    name: "Home",
    computed: {
        ...mapGetters(["getUser"])
    },
    mounted() {
		loadPlayer({
            url: `${this.$store.state.wsRootURL}/containers/api/stream/2`,
            canvas: document.getElementById('canvas'),

            // optional
            onDisconnect: () => console.log('Camera connection lost!'),
        });
    },
    
}
</script>

<style>
 .loader {
	height: 50vh;
	display: flex;
	justify-content: center;
	align-items: center;
}

#canvas {
    max-width: 50%;
    margin-left: 30%;
}

</style>