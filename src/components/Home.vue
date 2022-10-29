<template>
    <b-container fluid>
        <b-row class="m-2">
            <b-col sm v-if="getUser.role == 'ROLE_LEARNER'">
                <b-card img-fluid class="text-center booking-card cardClass" :img-src="require('../assets/calendar.png')">
                    <b-card-text style="font-size: 1.5rem">Find a time to access our robots and simulation environments!</b-card-text>
                    <b-button @click="$router.push({name: 'Booking'})" size="lg">Go to reservation</b-button>
                </b-card>
            </b-col>
            <b-col v-if="getUser.role == 'ROLE_LEARNER'">
                <b-img class="robotont-swarm" :src="require('../assets/robotonts.png')"></b-img>
            </b-col>
            <!-- <b-col v-if="getUser.role == 'ROLE_LEARNER'">
                <b-card style="max-width: 25vw" img-fluid class="text-center" :img-src="require('../assets/user_panel.png')" title="User Panel">
                    <b-card-text>View and start booked sessions</b-card-text>
                    <b-button @click="$router.push({name: 'UserPanel'})">View panel</b-button>
                </b-card>
            </b-col> -->
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/calendar.png')" title="Create slots">
                    <b-card-text>Create slots for booking system</b-card-text>
                    <b-button @click="$router.push({name: 'CreateSlot'})">Go create</b-button>
                </b-card>
            </b-col>
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/inventory.png')" title="Create inventory">
                    <b-card-text>Create inventory for robots and containers</b-card-text>
                    <b-button @click="$router.push({name: 'Inventory'})">View inventory</b-button>
                </b-card>
            </b-col>  
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/users.png')" title="Users">
                    <b-card-text>Edit users roles or activate/deactivate accounts</b-card-text>
                    <b-button @click="$router.push({name: 'Users'})">View users</b-button>
                </b-card>
            </b-col>
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/admin_panel.png')" title="Admin Panel">
                    <b-card-text>Admin Panel</b-card-text>
                    <b-button @click="$router.push({name: 'AdminPanel'})">View panel</b-button>
                </b-card>
            </b-col>
        </b-row>
        <UserPanel/>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import UserPanel from './UserPanel';

export default {
    name: "Home",
    computed: {
        ...mapGetters(["getUser"])
    },
    components: {
        UserPanel
    },
    mounted() {

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

.booking-card {
    border: 0 !important;
    max-width: 25vw !important;
    margin: 2rem 0 0 4rem;
}

.robotont-swarm {
    padding-top: 10rem;
    max-width: 60vw;
}

.opaque {
    opacity: 0.6;
}

.upcoming {
    background-color: #fdfbe7 !important;
}



@media screen and (min-width: 601px) {
        .cardClass {
            max-width: 30vw;
        }
    }

    @media screen and (max-width: 600px) {
        .cardClass {
            max-width: 100%;
        }
    }


</style>