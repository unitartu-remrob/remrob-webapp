<template>
    <b-container fluid>
        <b-row class="m-2">
            <b-col v-if="getUser.role == 'ROLE_LEARNER'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/calendar.png')" title="Book a slot">
                    <b-card-text>Book a robot or a container</b-card-text>
                    <b-button @click="$router.push({name: 'Booking'})">Go to booking</b-button>
                </b-card>
            </b-col>
            <b-col v-if="getUser.role == 'ROLE_LEARNER'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/user_panel.png')" title="User Panel">
                    <b-card-text>View and start booked sessions</b-card-text>
                    <b-button @click="$router.push({name: 'UserPanel'})">View panel</b-button>
                </b-card>
            </b-col>
            <b-col v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/calendar.png')" title="Create slots slot">
                    <b-card-text>Create slots for booking system</b-card-text>
                    <b-button @click="$router.push({name: 'CreateSlot'})">Go create</b-button>
                </b-card>
            </b-col>
            <b-col v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/inventory.png')" title="Create inventory">
                    <b-card-text>Create inventory for robots and containers</b-card-text>
                    <b-button @click="$router.push({name: 'Inventory'})">View inventory</b-button>
                </b-card>
            </b-col>  
            <b-col v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/users.png')" title="Users">
                    <b-card-text>Edit users roles or activate/deactivate accounts</b-card-text>
                    <b-button @click="$router.push({name: 'Users'})">View users</b-button>
                </b-card>
            </b-col>
            <b-col v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/admin_panel.png')" title="Admin Panel">
                    <b-card-text>Admin Panel</b-card-text>
                    <b-button @click="$router.push({name: 'AdminPanel'})">View panel</b-button>
                </b-card>
            </b-col>
        </b-row>
        <!-- <canvas id='canvas'>h264Preview_01_main</canvas> -->
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
		// loadPlayer({
        //     url: `${this.$store.state.wsRootURL}/containers/api/stream/2`,
        //     canvas: document.getElementById('canvas'),

        //     // optional
        //     onDisconnect: () => console.log('Camera connection lost!'),
        // });
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