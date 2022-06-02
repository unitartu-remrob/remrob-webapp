<template>
    <b-container fluid>
        <b-modal title="Create slot" @ok="createSlot" id="slot-modal">
            <b-form-group label="Start time">
                <b-form-timepicker v-model="start" locale="est"></b-form-timepicker>
            </b-form-group>
            <b-form-group label="End time">
                <b-form-timepicker v-model="end" locale="est"></b-form-timepicker>
            </b-form-group>
            <b-form-group label="Item">
                <b-form-select v-model="selectedInventory" :options="inventoryOptions"></b-form-select>
            </b-form-group>
        </b-modal>
        <b-modal ok-title="Confirm" title="Book the slot" id="booking-modal">
            <h4>Are you sure you want to book this slot?</h4>
        </b-modal>
        <div class="m-3">
            <FullCalendar :options="calendarOptions" />
        </div>
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
    name: "CreateSlot",
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
                select: this.handleDateSelect,
                eventClick: this.handleEventClick,
                eventsSet: this.handleEvents,
                eventDisplay: "block",
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
            inventoryOptions: [
                {value: 1, text: "Robot + Server"}
            ]
        };
    },
    methods: {
        handleEventClick: function (info) {
            console.log(info.event.id);
            this.$bvModal.show("booking-modal");
        },
        handleDateSelect: function (info) {
            console.log(info);
            this.selectedDate = info.startStr;
            this.$bvModal.show("slot-modal");
        },
        createSlot: function () {
            var slotData = {
                "start": this.selectedDate + "T" + this.start,
                "end": this.selectedDate + "T" + this.end,
                "inventoryId": this.selectedInventory
            }
            axios.post(this.$store.state.baseURL + "/bookings", slotData).then((res) => {
                this.getAllSlots()
            });
        },
        getAllSlots: function() {
            axios.get(this.$store.state.baseURL + "/bookings").then((res) => {
                console.log(res.data.bookings)
                this.calendarOptions.events = res.data.bookings
            });
        }
    },
    created() {
        this.getAllSlots()
    }
};
</script>

<style scoped></style>
