<template>
	<div class="containers-box">
		<h2 class="containers-title text-ubuntu-600">Simulation boxes</h2>
		<p class="text-ubuntu-500 text-center duration-notice">Simulation environments are open for one hour at a time.</p>
		<b-alert
			:show="showAlert"
			variant="danger"
			dismissible
			@dismissed="reset">
			{{errorMessage}}
		</b-alert>
		<div v-if="!activeContainer">
			<div v-for="item in publicContainers" :key="item.slug">
				<b-row align-h="center">
					<b-col>
						<Sandbox
							:container="item"
							:key="`${item.id}-${item.end_time}`"
							@container-claimed="storeClaimedContainer"
							@claim-error="showError"
							@session-expired="reset" />
					</b-col>
				</b-row>
			</div>
		</div>
		<div v-else class="active-session p-4">
			<div v-if="activeContainer" class="text-center">
				<h2>You have a claimed a simulation box:</h2>
			</div>
			<Sandbox v-if="activeContainer"
				:container="activeContainer"
				:key="`${activeContainer.id}-${activeContainer.end_time}`"
				activeSession=true
				@session-expired="reset"/>
			<b-button
				variant="success"
				@click="$router.push({ name: 'PublicSession', params: { container: activeContainer.slug } })"
				class="go-to-session-btn text-ubuntu-600">
				<ArrowRight />
				&nbsp;
				Go to session dashboard
			</b-button>
			<div class="d-flex justify-content-end text-ubuntu-600 mr-4">
				<b-button variant="dark" @click="yieldSession" class="m-4 terminate-session-btn">
					<Eject class="mr-2"/>
					Release
				</b-button>
			</div>
		</div>
		
	</div>
</template>

<script>
import Sandbox from './Sandbox.vue';

export default {
    name: 'PublicContainers',
    components: {
        Sandbox,
    },
    data() {
        return {
            activeContainer: null,
            publicContainers: [],

			showAlert: false,
			errorMessage: "",
        }
    },
    computed: {
        computedContainers: function() {
            return this.publicContainers;
        }
    },
    methods: {
        getPublicContainers: function() {
            this.$api.get('/containers/public-containers', {}).then((res) => {
                this.publicContainers = res.data;
                this.checkForActiveContainers();
            }).catch(err => {
				console.log("Error fetching public containers", err)
				this.showError(err);
			})
        },
        checkForActiveContainers: function() {
            this.publicContainers.forEach(container => {
                if (container.public_user) {
                    this.activeContainer = container;
                }
            });
        },
		reset: function() {
			this.showAlert = false; 
			this.activeContainer = null;
			this.getPublicContainers();
		},
        yieldSession: function() {
            if (!this.activeContainer) {
                return;
            }
            this.$api.delete(`/containers/claim/${this.activeContainer.slug}`, {}).then((_) => {
                this.reset();
				
            }).catch(err => {
                console.log("Error terminating session", err)
				this.showError(err);
				this.reset();
            })
        },
        storeClaimedContainer: function(container) {
            this.activeContainer = container;
            this.getPublicContainers();
        },
		showError: function(err) {
			this.errorMessage = err.response.data
			this.showAlert = true;
		}
    },
    created() {
        this.getPublicContainers();
    },
}
</script>

<style>

.duration-notice {
	font-size: 1.2rem;
}

.go-to-session-btn {
	font-size: 1.6rem !important;
	padding: 1rem 1.5rem !important;
	margin: 1rem 2rem;
	border-radius: 1rem !important;
}

.terminate-session-btn {
	padding: 0.25 0.75rem !important;
	border: 0px !important;
	background-color: rgba(95, 21, 56, 0.938) !important;
	margin: 1rem 2rem;
	border-radius: 0.5rem !important;
}

.containers-title {
	font-size: 2.2rem;
	color: rgb(66, 19, 64);
    text-align: center;
    margin-bottom: 1rem;
}

.containers-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 60%;
    margin-right: 5%;
}

.active-session {
    display: flex;
    flex-direction: column;
}

@media screen and (min-width: 1900px) {
	.duration-notice {
		font-size: 1.4rem;
	}
}

@media screen and (max-width: 1600px) {
	.duration-notice {
		font-size: 1rem;
	}
}

</style>