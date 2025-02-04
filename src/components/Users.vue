<template>
    <b-container fluid class="pt-3">
        <div class="text-center panel-title">Remrob userbase</div>
        <b-alert :show="dismissCountDown" dismissible @dismissed="dismissCountDown=0" @dismiss-count-down="countDownChanged" :variant="alertType" class="alert-float">{{message}}</b-alert>
        <b-modal ok-title="Confirm" @ok="deleteUser(selectedForDelete)" title="Delete user" id="delete-modal">
            <h4>Are you sure you want to delete this user?</h4>
        </b-modal>
        <b-row>
            <b-col>
                <b-table striped :items="users" :fields="fields">
                    <template #cell(role)="data">
                        <b-form-select @input="setRole(data.item.role, data.item.id)" :options="roles" v-model="data.item.role"></b-form-select>
                    </template>
                    <template #cell(active)="data">
                        <b-form-checkbox @input="setActive(data.item.active, data.item.id)" switch v-model="data.item.active"></b-form-checkbox>
                    </template>
                    <template #cell(files)="data">
                        <a v-if="data.item.owncloud_id" :href="oci(data.item.owncloud_id)"
                            target="_blank"
                            class="btn file-link"
                            :class="!oci(data.item.owncloud_id) ? 'disabled' : ''"
                            ><FilmIcon font-scale="1.4"/></a>
                        <a v-if="data.item.user_repo" :href="repo(data.item.user_repo)"
                            target="_blank"
                            class="btn"
                            :class="!oci(data.item.user_repo) ? 'disabled' : ''">
                            <JournalCode font-scale="1.6"/></a>
                    </template>
                    <template v-slot:cell(actions)="data">
                        <b-button @click="function() {selectedForDelete = data.item.id; $bvModal.show('delete-modal')}">Delete</b-button>
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
                { key: "files", label: "Student files" },
                { key: "role", label: "Role" },
                { key: "active", label: "Active" },
                { key: "actions", label: "Actions" }
            ],
            roles: [
                { value: "ROLE_ADMIN", text: "ADMIN" },
                { value: "ROLE_LEARNER", text: "ROS apprentice" }
            ],
            message: "",
            showAlert: false,
            dismissSec: 3,
            dismissCountDown: 0,
            alertType: "info",
            selectedForDelete: null
        }
    },
    computed: {
        ...mapGetters(["getUser"])
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
                this.alertType = 'info';
                this.dismissCountDown = this.dismissSec;
            })
        },
        oci(id) {
            if (id !== null && id.length) {
                return `https://owncloud.ut.ee/owncloud/s/${id}`
            }
        },
        repo(id) {
            if (id !== null && id.length) {
                return `https://gitlab.ut.ee/remrob/${id}`
            }
        },
        countDownChanged(dismissCountDown) {
            this.dismissCountDown = dismissCountDown
        },
    },

    created() {
        this.getUsers()
    }
    
}
</script>

<style>
.alert-float {
  position: fixed !important;
  top: 80px;
  left: 400px;
  right: 500px;
  border-radius: 20px !important;
  z-index: 1010;
}

</style>