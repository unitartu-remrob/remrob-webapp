<template>
    <b-container fluid class="panel">
        <div class="text-center panel-title">My sessions</div>
        <div class="loader" v-if="!this.is_loaded"><b-spinner style="width: 4rem; height: 4rem;" type="grow" variant="info"></b-spinner></div>
        <b-row v-else>
            <b-col>
                <b-table striped :items="bookings" :fields="fields">
                    <template v-slot:cell(join)="{ item }">
                        <b-button :disabled="!item.isActive" @click="$router.push({ name: 'Session', params: {session: item.id} })">Session dashboard</b-button>
                    </template>
                    <template v-slot:cell(start)="{ item }">
                        {{parseDate(item.start)}}
                    </template>
                    <template v-slot:cell(end)="{ item }">
                        {{parseDate(item.end)}}
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
        <b-row v-if="this.is_loaded && this.bookings.length === 0" class="no-session-message">
            You haven't reserved any time slots yet!
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import { getCountdown } from '../util/helpers'

export default {
    data() {
        return {
            fields: [
                // { key: "id", label: "Booking ID" },
                { key: "title", label: "" },
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
                // this.bookings.forEach(item => {
                //     item.start_time = item.start.slice(0, 16).replace("T", "  ")
                //     item.end_time = item.end.slice(0, 16).replace("T", "  ")
                // })
                this.bookings.sort((a, b) => (b.id - a.id))
                console.log(res.data)
            })			
        },
        parseDate: function(date) {
            return date.slice(0, 16).replace("T", "  ")
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
        this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
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
.panel {
    margin-bottom: 5rem;
}

.panel-title {
    font-size: 2rem;
    margin: 3.2rem 1rem 1.5rem;
    text-decoration: underline;
}

.loader {
    height: 15vh;
}

.no-session-message {
    font-size: 1.6rem;
    padding: 1rem;
    justify-content: center;
}
</style>