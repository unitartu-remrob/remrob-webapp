<template>
    <b-container class="sandbox-container">
        <b-card class="sandbox" :class="disableClass">
            <div class="remrob-box">
                <div class="text-ubuntu-500 mr-2 d-flex align-items-center">
                    <Box class="sim-box mr-3"/>
                    <div>
                        <h4 class="box-title">{{ this.container.slug }}</h4>
                        <span v-if="activeSessionContainer">(resource busy)</span>
                    </div>
                </div>
                <b-button
                    v-if="!activeSession && !this.occupied"
                    variant="success"
                    @click="claimContainer"
                    class="claim-ctn-btn">
                    Claim simulation box
                </b-button>
                <div v-if="sessionTime.isActive && (this.occupied || this.activeSession)" :key="timerKey" class="container-timer">
                    <div class="d-flex align-items-center">
                        <Clock variant="primary" class="timer-clock mr-2"/>    
                        <span>Time left: {{ sessionTime.displayTime }}</span>    
                    </div>
                </div>
                <div v-else-if="this.occupied || activeSession" class="placeholder ml-5"></div>
            </div>
        </b-card>
    </b-container>
</template>
  
<script>
import { getTimeLeft } from '../../util/helpers';

export default {
    name: 'Sandbox',
    props: ['container', 'activeSession'],
    data() {
        return {
            occupied: true,
            endTime: null,
            timer: "",
            timerKey: 0,
            sessionTime: {
                isActive: false,
                displayTime: "",
            },
        }
    },
    computed: {
        disableClass: function() {
            return this.activeSessionContainer ? 'opaque' : ''
        },
        activeSessionContainer: function() {
            return this.occupied & !this.activeSession;
        }
    },
    methods: {
        claimContainer: function() {
            this.$api.get(`/containers/claim/${this.container.slug}`, {}).then((res) => {
                const container = res.data;                
                this.$emit('container-claimed', container);
            }).catch(err => {
                console.log("Error claiming container", err)
                this.$emit("claim-error", err)
            })
        },
        timeLeft: function() {
            if (this.occupied) {
                const time = getTimeLeft(this.endTime);
                this.sessionTime.isActive = time.isActive;
                this.sessionTime.displayTime = time.displayTime;

                if (!time.isActive) {
                    clearInterval(this.timer);
                    this.$emit('session-expired')
                    this.$router.push({ name: 'Landing' })
                }
            }
        },
    },
    created() {
        this.occupied = this.container.occupied;
        this.endTime = this.container.end_time;
    },
    mounted() {
        this.timer = setInterval(this.timeLeft, 1000);
    },
    beforeDestroy() {  
        clearInterval(this.timer);
    },
}
</script>

<style>

.sandbox-container {
    margin-bottom: 2.5%;
    margin-top: 2.5%;
}

.sandbox {
    border: 4px solid cadetblue !important;
    border-radius: 2rem !important;
    background: rgb(250, 250, 250) !important;
}

.remrob-box {
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0.5rem;
}

.claim-ctn-btn {
    font-size: 1.3rem !important;
    padding: 0.5rem 1.5rem !important;
    margin-left: 15%;
}

.sim-box {
    font-size: 2.5rem;
}

.placeholder {
    width: 50%;
}

.busy-text {
    font-size: 1.3rem;
}

.container-timer {
    margin-left: 15%;
}

.container-timer span, .placeholder {
    font-weight: 600;
    font-size: 1.4rem;
}

.timer-clock {
    font-size: 1.5rem;
}

@media screen and (max-width: 1900px) {
    .box-title {
        font-size: 1.4rem;
    }
}

</style>