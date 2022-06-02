<template>
    <b-container fluid>
        <b-modal ok-title="Confirm" @ok="bookSlot" title="Book the slot" id="booking-modal">
            <h4>Are you sure you want to book this slot?</h4>
        </b-modal>
        <b-row class="text-center m-3">
            <b-col>
                <FullCalendar :options="calendarOptions" />
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import "@fullcalendar/core/vdom";
import FullCalendar /*{ CalendarOptions, EventApi, DateSelectArg, EventClickArg }*/ from "@fullcalendar/vue";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import axios from 'axios';

export default {
    name: "Booking",
    components: {
        FullCalendar,
    },
    data() {
        return {
            calendarOptions: {
                plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
                headerToolbar: {
                    left: "prev,next today",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek,timeGridDay",
                },
                initialView: "dayGridMonth",
                displayEventTime: true,
                editable: true,
                selectable: true,
                selectMirror: true,
                dayMaxEvents: false,
                weekends: true,
                eventDisplay: "block",
                select: this.handleDateSelect,
                eventClick: this.handleEventClick,
                eventsSet: this.handleEvents,
                events: [],
                eventTimeFormat: {
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false,
                },

            },
            
            start: null,
            end: null,
            selectedInventory: null,
            selectedDate: null,
            selectedSlot: null
        };
    },
    methods: {
        handleEventClick: function (info) {
            this.selectedSlot = info.event.id
            this.$bvModal.show("booking-modal");
        },
        handleDateSelect: function (info) {
            console.log(info);
        },
        bookSlot: function () {
            axios.post(this.$store.state.baseURL + "/bookings/book/" + this.selectedSlot, {"userId": this.$keycloak.subject}).then((res) => {
                this.getAllSlots()
            })
        },
        getAllSlots: function() {
            axios.get(this.$store.state.baseURL + "/bookings").then((res) => {
                console.log(res.data.bookings)
                this.calendarOptions.events = res.data.bookings
            });
            axios.get(this.$store.state.baseURL + "/bookings/" + this.$keycloak.subject).then((res) => {
                console.log(res.data.user_bookings)
                for (let i = 0; i < res.data.user_bookings.length; i++) {
                    this.calendarOptions.events.push(res.data.user_bookings[i])
                    
                }
            })
        },
    },
    created() {
        this.getAllSlots()
    }
};
</script>

<style scoped></style>
