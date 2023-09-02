<template>
    <b-container fluid>
        <b-modal centered hide-footer title="Choose creation mode" id="type-modal">
            <div class="text-center">
                <b-button @click="$bvModal.hide('type-modal'); $bvModal.show('slot-modal')" class="m-3">Single slot creation</b-button>
                <b-button @click="$bvModal.hide('type-modal'); $bvModal.show('bulk-modal')" class="m-3">Bulk slot creations</b-button>
                <div class="d-flex flex-column align-items-end mt-3">
                    <b-button @click="$bvModal.hide('type-modal'); $bvModal.show('delete-modal-date')" variant="outline-danger" pill size="sm">Delete all</b-button>
                </div>
            </div>
        </b-modal>
        <b-modal title="Create slots" @ok="createSlotsBulk" id="bulk-modal">
            <div class="px-2">
            <b-form-group>
                <b-row class="timepicker-row">
                    <b-col cols="6">
                        <label class="timepicker-label">Start time</label>
                        <VueTimepicker manual-input v-model="start"></VueTimepicker>
                    </b-col>
                    <b-col cols="6">
                        <label class="timepicker-label">End time</label>
                        <VueTimepicker manual-input v-model="end"></VueTimepicker>
                    </b-col>
                </b-row>
                <b-form-group class="mt-3" label="Session duration (minutes)">
                    <b-form-input type="number" placeholder="1" v-model="interval"></b-form-input>
                </b-form-group>
                <b-form-group class="mt-3" label="Number of concurrent sessions">
                    <b-form-input type="number" placeholder="1" v-model="nrOfSlots"></b-form-input>
                </b-form-group>
                <b-form-group class="mt-3" label="Downtime between sessions (minutes)">
                    <b-form-input type="number" placeholder="0" v-model="downtime"></b-form-input>
                    <div class="small mt-1">Adding pause between sessions will push the end time of the last session.</div>
                </b-form-group>
                
                <b-form-group label="Item">
                    <b-form-select v-model="selectedInventory" :options="inventory"></b-form-select>
                </b-form-group>
                <!-- <b-form-group label="Admin">
                    <b-form-checkbox-group v-model="selectedAdmin" :options="admins"></b-form-checkbox-group>
                </b-form-group> -->
            </b-form-group>
            </div>
        </b-modal>
        <b-modal title="Create slot" @ok="createSlot" id="slot-modal">
            <div class="px-2">
            <b-row class="timepicker-row">
                <b-col cols="6">
                    <label class="timepicker-label">Start time</label>
                    <VueTimepicker manual-input v-model="start"></VueTimepicker>
                </b-col>
                <b-col cols="6">
                    <label class="timepicker-label">End time</label>
                    <VueTimepicker manual-input v-model="end"></VueTimepicker>
                </b-col>
            </b-row>
            <b-form-group class="mt-3" label="Item">
                <b-form-select v-model="selectedInventory" :options="inventory"></b-form-select>
            </b-form-group>
            <!-- <b-form-group label="Admin">
                <b-form-checkbox-group v-model="selectedAdmin" :options="admins"></b-form-checkbox-group>
            </b-form-group> -->
            </div>
        </b-modal>
        <b-modal ok-title="Confirm" @ok="deleteSlot" title="Delete the slot" id="delete-modal">
            <h4>Are you sure you want to delete this slot?</h4>
        </b-modal>
        <b-modal ok-title="Confirm" @ok="deleteDate" title="Clear all slots of the day" id="delete-modal-date">
            <h4>Are you sure you want to delete all of this day's slots?</h4>
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
                locale: 'en-GB',
                firstDay: 1,
                displayEventTime: true,
                displayEventEnd: true,
                editable: false,
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
            interval: 60,
            downtime: 0,
            nrOfSlots: 1,
            admins: [],
            selectedAdmin: []
        };
    },
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
        eventRender: function(info) {
            var tooltip = new Tooltip(info.el, {
                title: "Admin: " + info.event.extendedProps.admin + "\n Student: " + info.event.extendedProps.user,
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
            this.$api.get("/api/v1/inventory").then((res) => {
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
            if (info.startStr.includes("T")){
                this.selectedDate = info.startStr.split("T")[0]
            }
            else {
                this.selectedDate = info.startStr
            }
            this.$bvModal.show("type-modal")
            //this.$bvModal.show("slot-modal");
        },
        createSlot: function () {
            var slotData = {
                "start": this.selectedDate + "T" + this.start,
                "end": this.selectedDate + "T" + this.end,
                "project": this.selectedInventory.project,
                "is_simulation": this.selectedInventory.simulation,
                "admin": this.selectedAdmin.join(", ")
            }
            this.$api.post("/api/v1/bookings", slotData).then((res) => {
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
                "nr_of_slots": this.nrOfSlots,
                "downtime": this.downtime,
                "admin": this.selectedAdmin.join(", ")
            }
            this.$api.post("/api/v1/bookings/bulk", slotData).then((res) => {
                this.getAllSlots()
            });

        },
        deleteDate: function() {
            console.log(this.selectedDate)
            this.$api.delete(`/api/v1/bookings/delete`, {
                data: {
                    "selected_day": this.selectedDate
                }
            }).then((res) => {
                this.getAllSlots()
            });
        },
        deleteSlot: function() {
            this.$api.delete(`/api/v1/bookings/delete/${this.selectedSlot}`).then((res) => {
                this.getAllSlots()
            });
        },
        getAllSlots: function() {
            this.$api.get(`/api/v1/slots`).then((res) => {
                this.calendarOptions.events = res.data.bookings
            });
        },

        getAdmins: function() {
          this.$api.get(`/api/v1/admins`).then((res) => {
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

<style>
.fc-event{
    cursor: pointer;
}

.tooltip-inner {
    white-space: pre-wrap;
}

.timepicker-label {
  margin-bottom: 3px;
}
/* 
.timepicker-row {
  margin-right: -5px;
  margin-left: -5px;
} */

/* .timepicker-row > .col-6 {
  padding-right: 5px;
  padding-left: 5px;
} */
</style>
