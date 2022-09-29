<template>
  <b-nav-item :disabled="!owncloud_active" target="_blank" rel="" :href="this.owncloud_link">
    <b-button :disabled="!owncloud_active">My submissions</b-button>
  </b-nav-item>
</template>

<script>
import axios from 'axios'

export default {
  // props: ['robotID'],
  data() {
    return {
      owncloud_active: false,
      owncloud_link: null,
    }
  },
  computed: {
    
  },
  methods: {
    getOwncloudLink: function() {
      axios.get(this.$store.state.baseURL + "/owncloud_link", {headers: this.$store.state.header}).then((res) => {
        this.owncloud_active = true;
        this.owncloud_link = res.data;
      }).catch(e => {
        console.log(e)
      })
    }
  },
  created() {
    this.getOwncloudLink()
  },
}
</script>

<style>

</style>