<template>
    <b-container fluid>
        <b-row class="text-center m-3">
            <b-col>
                <b-card style="max-width: 30vw" img-fluid class="text-center" :img-src="require('../assets/calendar.png')" title="Book a slot">
                    <b-card-text>Book a robot or a container</b-card-text>
                    <b-button @click="$router.push({name: 'Booking'})">Go to booking</b-button>
                </b-card>
            </b-col>
            <b-col>
                <h3>List of bookings</h3>
            </b-col>
        </b-row>

    </b-container>
</template>

<script>
export default {
    name: "Home",
    mounted() {
        console.log(this.$keycloak.loadUserInfo())
        console.log(this.$keycloak)
    }
    
}
</script>

<style lang="scss" scoped>

</style>