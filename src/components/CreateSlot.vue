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
                <b-form-select v-model="selectedInventory" :options="inventory"></b-form-select>
            </b-form-group>
        </b-modal>
        <b-modal ok-title="Confirm" title="Delete the slot" id="delete-modal">
            <h4>Are you sure you want to delete this slot?</h4>
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
import { mapGetters } from 'vuex';

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
            inventory: []
        };
    },
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        getOptions: function(inv) {
            const getInstances = ({ project }, data) => data.filter(d => d.project === project).length
            const optionCount = inv.reduce((group, item, i, stock) => {
                const alreadyCounted = group.some(({ project }) => project === item.project)
                if (!alreadyCounted) {
                    group.push({
                        project: item.project,
                        id: item.robot_id,
                        count: getInstances(item, stock)
                    })
                }
                return group
            }, [])
            return optionCount
        },
        getInventory: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/inventory", {headers: this.$store.state.header}).then((res) => {
                const options = this.getOptions(res.data);
                for (let i = 0; i < options.length; i++) {
                    this.inventory.push({value: {
                        simulation: false,
                        project: options[i].project
                    }, text: `Robotont@${options[i].project} (x${options[i].count})`})
                }
                this.inventory.push({value: {
                    simulation: true,
                    project: "simulation"
                }, text: "Simulation (x9)"})
            })
        },
        handleEventClick: function (info) {
            console.log(info.event.id);
            this.$bvModal.show("delete-modal");
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
                "project": this.selectedInventory.project,
                "is_simulation": this.selectedInventory.simulation
            }
            console.log(slotData)
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.post(this.$store.state.baseURL + "/bookings", slotData, {headers: this.$store.state.header}).then((res) => {
                this.getAllSlots()
            });
        },
        getAllSlots: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/bookings", {headers: this.$store.state.header}).then((res) => {
                this.calendarOptions.events = res.data.bookings
            });
        }
    },
    created() {
        this.getAllSlots()
        this.getInventory()
    }
};
</script>

<style scoped></style>
