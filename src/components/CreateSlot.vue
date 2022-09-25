<template>
    <b-container fluid>
        <b-modal centered hide-footer title="Choose creation type" id="type-modal">
            <div class="text-center">
                <b-button @click="$bvModal.hide('type-modal'); $bvModal.show('slot-modal')" class="m-3">Single slot creation</b-button>
                <br>
                <b-button @click="$bvModal.hide('type-modal'); $bvModal.show('bulk-modal')" class="m-3">Bulk slot creations</b-button>
            </div>
        </b-modal>
        <b-modal title="Create slots" @ok="createSlotsBulk" id="bulk-modal">
            <b-form-group label="Start time">
                <VueTimepicker manual-input v-model="start"></VueTimepicker>
            </b-form-group>
            <b-form-group label="End time">
                <VueTimepicker manual-input v-model="end"></VueTimepicker>
            </b-form-group>
            <b-form-group label="Time interval (hour)">
                <b-form-input type="number" placeholder="1" v-model="interval"></b-form-input>
            </b-form-group>
            <b-form-group label="Item">
                <b-form-select v-model="selectedInventory" :options="inventory"></b-form-select>
            </b-form-group>
            <b-form-group label="Admin">
                <b-form-select v-model="selectedAdmin" :options="admins"></b-form-select>
            </b-form-group>
        </b-modal>
        <b-modal title="Create slot" @ok="createSlot" id="slot-modal">
            <b-form-group label="Start time">
                <VueTimepicker format="HH:mm" manual-input v-model="start"></VueTimepicker>
            </b-form-group>
            <b-form-group label="End time">
                <VueTimepicker manual-input v-model="end"></VueTimepicker>
            </b-form-group>
            <b-form-group label="Item">
                <b-form-select v-model="selectedInventory" :options="inventory"></b-form-select>
            </b-form-group>
            <b-form-group label="Admin">
                <b-form-select v-model="selectedAdmin" :options="admins"></b-form-select>
            </b-form-group>
        </b-modal>
        <b-modal ok-title="Confirm" @ok="deleteSlot" title="Delete the slot" id="delete-modal">
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
import {Tooltip} from 'bootstrap'
import VueTimepicker from 'vue2-timepicker/src/vue-timepicker.vue';

export default {
    name: "CreateSlot",
    components: {
        FullCalendar,
        VueTimepicker
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
                displayEventEnd: true,
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
                eventDidMount: this.eventRender,
                eventTimeFormat: {
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false,
                },
            },
            start: '',
            end: '',
            selectedInventory: null,
            selectedDate: null,
            selectedSlot: null,
            inventory: [],
            interval: 1,
            admins: [],
            selectedAdmin: ""
        };
    },
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        eventRender: function(info) {
            var tooltip = new Tooltip(info.el, {
                title: "Admin: " + info.event.extendedProps.admin,
                placement: 'top',
                trigger: 'hover',
                container: 'body'
            });
        },

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
            this.selectedSlot = info.event.id
            this.$bvModal.show("delete-modal");
        },
        handleDateSelect: function (info) {
            this.selectedDate = info.startStr;
            this.$bvModal.show("type-modal")
            //this.$bvModal.show("slot-modal");
        },
        createSlot: function () {
            var slotData = {
                "start": this.selectedDate + "T" + this.start,
                "end": this.selectedDate + "T" + this.end,
                "project": this.selectedInventory.project,
                "is_simulation": this.selectedInventory.simulation,
                "admin": this.selectedAdmin
            }
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.post(this.$store.state.baseURL + "/bookings", slotData, {headers: this.$store.state.header}).then((res) => {
                this.getAllSlots()
            });
        },

        createSlotsBulk: function() {
            var slotData = {
                "start": this.selectedDate + "T" + this.start,
                "end": this.selectedDate + "T" + this.end,
                "interval": this.interval,
                "project": this.selectedInventory.project,
                "is_simulation": this.selectedInventory.simulation,
                "admin": this.selectedAdmin
            }
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.post(this.$store.state.baseURL + "/bookings/bulk", slotData, {headers: this.$store.state.header}).then((res) => {
                this.getAllSlots()
            });

        },

        deleteSlot: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.delete(this.$store.state.baseURL + "/bookings/delete/" + this.selectedSlot, {headers: this.$store.state.header}).then((res) => {
                this.getAllSlots()
            });
        },
        getAllSlots: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/slots", {headers: this.$store.state.header}).then((res) => {
                this.calendarOptions.events = res.data.bookings
            });
        },

        getAdmins: function() {
            this.$store.state.header.Authorization = "Bearer " + this.getUser.access_token
            axios.get(this.$store.state.baseURL + "/admins", {headers: this.$store.state.header}).then((res) => {
                for (let i = 0; i < res.data.length; i++) {
                    this.admins.push({value: res.data[i], text: res.data[i]})
                }
            });
        }
    },
    created() {
        this.getAllSlots()
        this.getInventory()
        this.getAdmins()
    }
};
</script>

<style scoped></style>
