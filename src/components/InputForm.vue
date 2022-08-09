<template>
	<div class="d-flex">
		<b-form-input :disabled="!edit" v-model="inventoryItem.project" class="w-50 d-inline mr-3"></b-form-input>
		<div>
			<b-button :disabled="edit" class="mr-2" type="button" @click="editField()">Edit</b-button>
			<b-button :disabled="!edit" type="button" @click="updateField()">Save</b-button>
		</div>
	</div>
</template>

<script>

export default {
	props: ['inventoryItem'],
	data: function() {
		return {
			edit: false
		}
	},
	methods: {
		editField: function() {
			this.edit = true
		},
		updateField: function() {
			this.$emit('update', {
				...this.inventoryItem
			})
			this.edit = false
		}
	},
	created: function() {

	},
}
</script>

<style>

</style>