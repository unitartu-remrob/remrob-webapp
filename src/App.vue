<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" sticky variant="dark">
      <b-navbar-brand style="cursor:pointer" @click="$router.push({name:'Home'})">Remrob</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <!-- <b-nav-item>
          <b-button @click="$keycloak.logout()">Logout</b-button>
        </b-nav-item> -->
      </b-navbar-nav>
    </b-navbar>
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
    
  }
}
</script>

<style>

</style>
