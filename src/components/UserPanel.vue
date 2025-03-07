<template>
    <b-container fluid class="panel">
        <div class="text-center panel-title">My sessions</div>
        <div class="loader" v-if="!this.is_loaded"><b-spinner style="width: 4rem; height: 4rem;" type="grow" variant="info"></b-spinner></div>
        <b-row v-else>
            <b-col>
                <b-table
                :items="bookings"
                :fields="fields"
                striped
                outlined
                head-variant="dark"
                :tbody-tr-class="rowClass"
                class="session-table">
                    <template v-slot:cell(join)="{ item }">
                        <b-button
                            :disabled="!item.isActive"
                            @click="$router.push({ name: 'Session', params: {session: item.id} })"
                            style="font-size: 1.3rem; padding: 0.5rem 1.5rem;">
                            Session dashboard
                        </b-button>
                    </template>
                    <template v-slot:cell(title)="{ item }">
                        <div class="d-flex mr-4 align-items-center ml-4">
                            <b-img v-if="item.is_simulation" class="slot-icon" :src="require('../assets/robotont-sim.png')"></b-img>
                            <b-img v-else class="slot-icon" :src="require('../assets/robotont-right.png')"></b-img>
                            <span class="booking-title ml-5" style="font-size: 1.5rem;">{{ item.title }}</span>
                        </div>
                    </template>
                    <template v-slot:cell(start)="{ item }">
                        <Clock variant="primary" />
                        {{ getDateFromDateTime(item.start) }}
                    </template>
                    <template v-slot:cell(end)="{ item }">
                        <Clock variant="primary"/>
                        {{ getDateFromDateTime(item.end) }}
                    </template>
                    <template v-slot:cell(countdown)="{ item }">
                        <div :key="timerKey" class="timer">            
                            <span v-if="!item.isActive && !item.isExpired">Starts in: {{ item.displayTime }}</span>
                            <span v-else-if="!item.isExpired">Time left: {{ item.displayTime }}</span>
                            <span v-else>Finished</span>
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
import { getCountdown } from '../util/helpers'
import { getDateFromDateTime } from '../util/helpers';

export default {
    data() {
        return {
            fields: [
                { key: "title", label: "", tdClass: 'align-middle', thStyle: { width: "25%" },},
				{ key: "start", label: "Starts", tdClass: 'align-middle'},
				{ key: "end", label: "Ends", tdClass: 'align-middle'},
                { key: "countdown", label: "", tdClass: 'align-middle'},
                { key: "join", label: "", tdClass: 'align-middle' },
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
        rowClass(item, type) {
            if (!item || type !== 'row') return
            if (item.isActive) return 'table-success'
            else if (item.isExpired) return 'opaque'
            else return 'upcoming'
        },
        getBookings: function() {
            this.$api.get(`/api/v1/bookings/${this.getUser.user_id}`).then((res) => {
                this.bookings = res.data.user_bookings

                this.bookings.sort((a, b) => (b.id - a.id))
                console.log(res.data)
            })			
        },
        getDateFromDateTime,
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
.panel {
    margin-bottom: 5rem;
    margin-top: 4rem;
    font-size: 1.2rem;
    max-width: 85%;
    padding: 0.5rem 3rem 1rem;
    position: relative;
    z-index: 30;
}


.panel-title {
    position: absolute;
    top: -1.6rem;
    /* top: -5.6%; */
    left: calc(-4rem - 6rem);
    /* padding: 1.1rem 3.5rem; */
    padding: 1.2% 4%;
    background-color: #cfaa05;
    color: white;
    font-size: 1.8rem;
    font-weight: 600;
    z-index: 50;
    box-shadow: -13px -23px 133px -22px rgba(0,0,0,0.75);
}

.session-table {
    background-color: white;
    border: 0 !important;
    box-shadow: 1px -1px 117px 3px rgba(0,0,0,0.75);
}

.loader {
    height: 15vh;
}

.slot-icon {
    max-width: 4rem;
    margin-left: 1rem;
}

.timer > p {
    display: flex;
    align-items: center;
}

.table-success .timer span,
.upcoming .timer span {
    font-weight: bold;
    font-size: 1.35rem;
}

.no-session-message {
    font-size: 1.6rem;
    padding: 1rem;
    justify-content: center;
}
</style>