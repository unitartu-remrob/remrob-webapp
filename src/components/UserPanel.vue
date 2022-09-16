<template>
    <b-container fluid>
		<br><br><br>
        <br><br><br><br>
        <b-row>
            <b-col>
                <div class="loader" v-if="!this.is_loaded"><b-spinner style="width: 5rem; height: 5rem;" type="grow" variant="info"></b-spinner></div>
                <b-table v-else striped :items="bookings" :fields="fields">
                    <template v-slot:cell(join)="{ item }">
                        <b-button :disabled="!item.isActive" @click="$router.push({ name: 'Session', params: {session: item.id} })">Session dashboard</b-button>
                    </template>
                    <template v-slot:cell(countdown)="{ item }">
                        <div :key="timerKey">                   
                            <p v-if="!item.isActive && !item.isExpired">Starts in: {{ item.displayTime }}</p>
                            <p v-else-if="!item.isExpired">Time left: {{ item.displayTime }}</p>
                            <p v-else>Finished</p>
                        </div>
                    </template>
                </b-table>
            </b-col>
        </b-row>

    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import { getCountdown } from '../util/helpers'
axios.defaults.withCredentials = true

export default {
    data() {
        return {
            fields: [
                // { key: "id", label: "Booking ID" },
                { key: "title", label: "Project" },
				{ key: "start", label: "Start" },
				{ key: "end", label: "End" },
                { key: "countdown", label: "" },
                { key: "join", label: "" },
            ],
            bookings: [],
            timerKey: 0,
            timer: "",
            is_loaded: false
        }
    },   
    computed: {
        ...mapGetters(["getUser"]),
    },
    methods: {
        getBookings: function() {
            axios.get(`${this.$store.state.baseURL}/bookings/${this.getUser.user_id}`, {headers: this.$store.state.header}).then((res) => {
                this.bookings = res.data.user_bookings
                this.bookings.forEach(item => {
                    item.start = item.start.slice(0, 16).replace("T", "  ")
                    item.end = item.end.slice(0, 16).replace("T", "  ")
                })
                this.bookings.sort((a, b) => (b.id - a.id))
                console.log(res.data)
            })			
        },
        updateTime() {
            this.bookings.forEach(booking => {
                const { start, end } = booking;
                const time = getCountdown(start, end);
                booking = Object.assign(booking, time)
            });
            this.is_loaded = true
            this.timerKey += 1;
        }
    },
    created() {
          this.getBookings();
    },
    mounted() {
        this.timer = setInterval(this.updateTime, 1000);
    },
    beforeDestroy() {  
        clearInterval(this.timer);
    },  
}
</script>

<style scoped>

</style>