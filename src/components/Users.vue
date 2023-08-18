<template>
    <b-container fluid class="mt-3">
        <b-alert :show="dismissCountDown" dismissible @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged" :variant="alertType" class="alert-float">{{message}}</b-alert>
        <b-modal ok-title="Confirm" @ok="deleteUser(selectedForDelete)" title="Delete user" id="delete-modal">
            <h4>Are you sure you want to delete this user?</h4>
        </b-modal>
        <b-row>
            <b-col>
                <b-table striped :items="users" :fields="fields">
                    <template #cell(role)="data">
                        <b-form-select @input="setRole(users[data.index].role, users[data.index].id)" :options="roles" v-model="users[data.index].role"></b-form-select>
                    </template>
                    <template #cell(active)="data">
                        <b-form-checkbox @input="setActive(users[data.index].active, users[data.index].id)" switch v-model="users[data.index].active"></b-form-checkbox>
                    </template>
                    <template v-slot:cell(actions)="data">
                        <b-button @click="function() {selectedForDelete = users[data.index].id; $bvModal.show('delete-modal')}">Delete</b-button>
                    </template>
                </b-table>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    data() {
        return {
            users: null,
            fields: [
                { key: "id", label: "User ID" },
                { key: "first_name", label: "First Name" },
                { key: "last_name", label: "Last Name" },
                { key: "email", label: "Email" },
                { key: "role", label: "Role" },
                { key: "active", label: "Active" },
                {key: "actions", label: "Actions"}
            ],
            roles: [
                {value: "ROLE_ADMIN", text: "ADMIN"},
                {value: "ROLE_LEARNER", text: "ROS apprentice"}
            ],
            message: "",
            showAlert: false,
            dismissSec: 3,
            dismissCountDown: 0,
            alertType: "",
            selectedForDelete: null
        }
    },
    computed: {
        ...mapGetters(["getUser"]),
    },
    methods: {
        getUsers: function() {
            this.$api.get("/api/v1/users").then((res) => {
                this.users = res.data
            })
        },
        deleteUser: function(id) {
            this.$api.delete(`/api/v1/users/${id}`).then((res) => {
                this.message = res.data
                this.alertType = "info"
                this.dismissCountDown = this.dismissSec;
                this.getUsers()
            })
        },
        setActive: function(active, id) {
            const data = { id, active }
            this.$api.put("/api/v1/users", data).then((res) => {
                this.message = res.data
                // this.showAlert = true;
                this.alertType = active ? "success" : "warning";
                this.dismissCountDown = this.dismissSec;
            })

        },
        setRole: function(role, id) {
            const data = {id, role}
            this.$api.put("/api/v1/users", data).then((res) => {
                this.message = res.data;
                this.dismissCountDown = this.dismissSec;
            })
        }
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },

    created() {
        this.getUsers()
    }
    
}
</script>

<style>
.alert-float {
  position: fixed !important;
  top: 80px; /* Adjust top position as needed */
  left: 400px; /* Adjust right position as needed */
  right: 500px;
  border-radius: 20px !important;
  z-index: 1010; /* Adjust z-index as needed */
}

</style>