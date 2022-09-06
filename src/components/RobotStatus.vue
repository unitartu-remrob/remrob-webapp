<template>
	<div>
		<div class="robot-status mt-5">Robot status</div>
    <div class="d-flex justify-content-center mt-3">
      <CircleFill v-if="this.robotStatus === 'true'" class="status-indicator" variant="success" font-scale="2" />
      <CircleFill v-else variant="danger" font-scale="2" />
    </div>
	</div>
</template>

<script>

export default {
  props: ['robotID'],
  data() {
    return {
      ws: null,
      robotStatus: null,
    }
  },

  computed: {
    
  },
  methods: {
    connectWs: function() {
			const ws = new WebSocket(`${this.$store.state.wsRootURL}/containers/robot-status/${this.robotID}`) // TODO: add cookie auth
			ws.onmessage = (event) => {
        this.robotStatus = event.data
        console.log(event.data)
			}
			ws.onopen = function(event) {
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
	font-weight: 700;
  font-size: 1.4rem;
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