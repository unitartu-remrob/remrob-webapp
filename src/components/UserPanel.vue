<template>
    <b-container fluid>
		<br><br><br>
		<b-row>
            <b-col>
                USER HERE
            </b-col>
        </b-row>
        <br><br><br><br>
        <b-row>
            <b-col>
                <b-table striped :items="inventory"></b-table>
            </b-col>
        </b-row>

    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
export default {
    data() {
        return {
            inventory: ["Here", "be", "dragons"]
        }
    },   
    computed: {
        ...mapGetters(["getUser"])
    },
    methods: {
    
    },
    created() {

    }
}
</script>

<style lang="scss" scoped>

</style>