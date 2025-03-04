<template>
	<div class="d-flex align-items-center">

		<label v-if="!isSimtainer" for="workcell" class="mr-2 mb-0">Workcell:</label>
		<b-form-input v-if="!isSimtainer" :disabled="!edit" v-model="inventoryItem.cell" type="number" id="workcell" class="w-25 d-inline mr-3"></b-form-input>
		
		<!-- <label for="project" class="mr-2 mb-0">Project:</label>
		<b-form-input :disabled="!edit" v-model="inventoryItem.project" id="project" class="w-25 d-inline mr-3"></b-form-input> -->
		<b-form-checkbox :disabled="!edit" class="mr-4 ml-4"
			switch
			v-model="itemStatus"
			/>
		<div>
			<b-button :disabled="edit" class="mr-2" type="button" @click="editField()">Edit</b-button>
			<b-button :disabled="!edit" type="button" @click="updateField()">Save</b-button>
		</div>
	</div>
</template>

<script>

export default {
	props: ['inventoryItem', 'isSimtainer'],
	data: function() {
		return {
			edit: false,
			itemStatus: null,
		}
	},
	computed: {

	},
	methods: {
		editField: function() {
			this.edit = true
		},
		updateField: function() {
			const updatedStatus = this.isSimtainer ? { open_to_public: this.itemStatus } : { status: this.itemStatus }
			this.$emit('update', {
				...this.inventoryItem,
				...updatedStatus
			})
			this.edit = false
		}
	},
	created: function() {
		if (this.isSimtainer) {
			this.itemStatus = this.inventoryItem.open_to_public
		} else {
			this.itemStatus = this.inventoryItem.status
		}
	},
}
</script>

<style>

</style>