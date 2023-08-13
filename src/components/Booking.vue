<template>
    <b-container fluid>
        <b-modal ok-title="Confirm" @ok="deleteBooking" title="Delete booking" id="delete-booking-modal">
            <h4>Are you sure you want to delete your booking?</h4>
        </b-modal>
        <b-modal ok-title="Confirm" @ok="bookSlot" title="Book the slot" id="booking-modal">
            <h4>Are you sure you want to book this slot?</h4>
        </b-modal>
        <b-alert class="m-2"
            :show="dismissCountDown"
            dismissible
            @dismissed="dismissCountDown=0"
            @dismiss-count-down="countDownChanged"
            variant="danger"
        >{{errorMessage}}
        </b-alert>
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
import { Tooltip } from 'bootstrap'
import { mapGetters } from 'vuex';

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
                locale: 'en-GB',
                firstDay: 1,
                displayEventTime: true,
                displayEventEnd: true,
                editable: false,
                selectable: true,
                selectMirror: true,
                dayMaxEvents: false,
                weekends: true,
                eventDidMount: this.eventRender,
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
            selectedSlot: null,  
            showAlert: false,
            dismissSec: 5,
            dismissCountDown: 0,
            errorMessage: null,   
        };
    },
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        handleEventClick: function (info) {
            if (new Date(info.event.startStr) < new Date() && new Date(info.event.endStr) < new Date()) {
                return;
            }

            this.selectedSlot = info.event.id
            if (info.event.backgroundColor === "green") {
                this.$bvModal.show("delete-booking-modal")
            }
            else {
                this.$bvModal.show("booking-modal");
            }
        },

        eventRender: function(info) {
            var tooltip = new Tooltip(info.el, {
                title: "Admin: " + info.event.extendedProps.admin,
                placement: 'top',
                trigger: 'hover',
                container: 'body'
            });
        },

        handleDateSelect: function (info) {
            console.log(info);
        },
        countDownChanged(dismissCountDown) {
            this.dismissCountDown = dismissCountDown
        },

        bookSlot: function () {
            const data = {"userId": this.getUser.user_id}
            this.$api.post(`/api/v1/bookings/book/${this.selectedSlot}`, data).then((res) => {
                this.getAllSlots()
            }).catch((error) => {
                this.errorMessage = error.response.data
                this.dismissCountDown = this.dismissSec
            })
        },
        deleteBooking: function() {
            this.$api.delete(`/api/v1/bookings/unbook/${this.getUser.user_id}/${this.selectedSlot}`).then((res) => {
                this.getAllSlots()
            })
        },
        getAllSlots: function() {
            this.calendarOptions.events = []
            this.$api.get(`/api/v1/bookings`).then((res) => {
                for (let i = 0; i < res.data.bookings.length; i++) {
                    this.calendarOptions.events.push(res.data.bookings[i])
                }
            });
            this.$api.get(`/api/v1/bookings/${this.getUser.user_id}`).then((res) => {
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

<style>
.fc-event{
    cursor: pointer;
}
</style>
