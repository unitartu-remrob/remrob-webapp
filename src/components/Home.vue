<template>
    <b-container fluid>
        <div
        class="bg-main"
        :class="getUser.role == 'ROLE_ADMIN' ? 'bg-main' : 'bg-cell'"></div>
        <b-row class="admin-menu">
            <b-col sm v-if="getUser.role == 'ROLE_LEARNER'">
                <b-card img-fluid class="text-center booking-card cardClass" :img-src="require('../assets/calendar.png')">
                    <b-card-text style="font-size: 1.4rem">Find a time to access our robots and simulation environments!</b-card-text>
                    <b-button @click="$router.push({name: 'Booking'})" size="lg" variant="">Go to reservation</b-button>
                </b-card>
            </b-col>
            <b-col v-if="getUser.role == 'ROLE_LEARNER'">
                <InfoPanel/>
            </b-col>
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/calendar.png')" title="Create slots">
                    <b-card-text>Create bookable time slots for learners.</b-card-text>
                    <b-button @click="$router.push({name: 'CreateSlot'})">Slot creation</b-button>
                </b-card>
            </b-col>
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/inventory.png')" title="Manage inventory">
                    <b-card-text>Manage robot placement and access.</b-card-text>
                    <b-button @click="$router.push({name: 'Inventory'})">View inventory</b-button>
                </b-card>
            </b-col>  
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/users.png')" title="Users">
                    <b-card-text>Edit users roles or activate/deactivate accounts.</b-card-text>
                    <Counter endpoint="users">
                        <b-button @click="$router.push({name: 'Users'})">View users</b-button>
                    </Counter>
                </b-card>
            </b-col>
            <b-col sm v-if="getUser.role == 'ROLE_ADMIN'">
                <b-card img-fluid class="text-center" :img-src="require('../assets/admin_panel.png')" title="Admin Panel">
                    <b-card-text>Monitor user sessions.</b-card-text>
                    <Counter endpoint="inventory">
                      <b-button @click="$router.push({name: 'AdminPanel'})">View panel</b-button>
                    </Counter>
                </b-card>
            </b-col>
        </b-row>
        <UserPanel/>
    </b-container>
</template>

<script lang="js">
import { mapGetters } from 'vuex';
import UserPanel from './UserPanel';
import Counter from './Counter';
import InfoPanel from './Newsboard/InfoPanel';

export default {
    name: "Home",
    computed: {
        ...mapGetters(["getUser"])
    },
    components: {
        UserPanel,
        Counter,
        InfoPanel
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

.panel-title {
    font-size: 2.3rem;
    margin: 1rem 10rem 1.5rem;
}

.opaque {
    opacity: 0.6;
}

.upcoming {
    background-color: #fdfbe7 !important;
}

.bg-main {
    background-image: url('../assets/login_bg.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    background-attachment: fixed;
    box-sizing: border-box;
    position: fixed;
    z-index: -5;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    opacity: 0.9;
    will-change: transform;
}

.bg-cell {
    background-image: url('../assets/cell.jpg');
}

.admin-menu {
    padding: 0.5rem;
    position: relative;
    margin: 2rem auto 1rem !important;
    max-width: 85%;
}

.admin-menu .card {
    background-color: rgba(255, 255, 255, 0.65);
    border: 6px solid rgb(22, 20, 20);
    border-radius: 2rem;
    padding: 1rem 2rem;
    height: calc(100% - 0.5rem);
}

.admin-menu .card-title {
    font-size: 1.6rem;
    font-weight: bold;
    /* margin-top: 4px; */
}

.admin-menu .card-text {
    font-size: 1rem;
    font-weight: 500;
}

@media screen and (min-width: 601px) {
    .admin-menu .booking-card {
        align-items: center;
        max-width: 22vw;
        margin: 0 0 0 4rem;
        padding: 1.6rem 2rem;
        background-color: rgba(255, 255, 255, 0.9);
        z-index: 30;
    }
    .booking-card .card-img {
        width: 75%;
        
    }
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