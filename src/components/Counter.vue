<template>
  <div class="counter">
    <slot></slot>
    <span class="counter-badge" v-if="counter > 0">{{ counter }}</span>
  </div>
</template>

<script>
export default {
  name: 'counter',
  props: {
    endpoint: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      counter: 0
    };
  },
  methods: {
    fetchCounterData() {
      // Make an API call to the backend using the specified endpoint
      // Update the counter value based on the response
      
      if (this.endpoint == "users") {
        const params = new URLSearchParams([['active', false]]);
        this.$api.get("/api/v1/users", {params}).then((res) => {
          const users = res.data;
          this.counter = users.length;
        })
      }
      else if (this.endpoint == "inventory") {
        const params = new URLSearchParams([['user', 'true']]);
        this.$api.get("/api/v1/inventory", {params}).then((res) => {
          const inventory = res.data;
          this.counter += inventory.length;
        })
        this.$api.get("/api/v1/simtainers", {params}).then((res) => {
          const sim_inventory = res.data;
          this.counter += sim_inventory.length;
        })
      }
    }
  },
  mounted() {
    this.fetchCounterData();
  },
}
</script>

<style scoped>
.counter {
  position: relative;
  display: inline-block;
}

.counter-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  padding: 4px 10px;
  background-color: #17a2b8;
  color: white;
  border-radius: 50%;
  font-size: 13px;
  font-weight: 600;
}
</style>