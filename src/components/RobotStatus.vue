<template>
    <div class="robot-status">
        <div class="indicator"> ⚡ Robot status ⚡</div>
        <div class="d-flex justify-content-center mt-3 mb-3 indicator">
            <CircleFill v-if="this.robotStatus === 'true'" class="status-indicator" variant="success" font-scale="1.5"/>
            <CircleFill v-else variant="danger" font-scale="1.5"/>
        </div>
        <!-- <b-img style="max-width: 12vw" :src="require('../assets/robotont.png')"></b-img> -->
    </div>
</template>

<script>

import {wsRootURL} from "@/util/api";

export default {
    props: ['robotID'],
    data() {
        return {
            ws: null,
            robotStatus: null,
        }
    },

    computed: {},
    methods: {
        connectWs: function () {
            const ws = new WebSocket(`${wsRootURL}/containers/robot-status/${this.robotID}`) // TODO: add cookie auth
            ws.onmessage = (event) => {
                this.robotStatus = event.data
                console.log(event.data)
            }
            ws.onopen = function (event) {
                console.log("Streaming robot status...")
            }
            this.ws = ws; // ref for closing
        }
    },
    created() {
        this.connectWs()
    },
    beforeDestroy() {
        this.ws.close()
    }
}
</script>

<style>
.robot-status {
    display: flex;
    flex-direction: column;
    text-align: center;
    margin-left: 7rem;
    font-weight: 700;
    font-size: 1.6rem;
}

.robot-status .indicator {
    font-size: 2rem;
}

.status-indicator {
    animation: blink 1.5s infinite;
}

@keyframes blink {
    0% {
        opacity: 0;
    }
    35% {
        opacity: 1;
    }
    75% {
        opacity: 0.8;
    }
    100% {
        opacity: 0;
    }
}
</style>