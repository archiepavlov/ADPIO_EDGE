<script  lang="ts">
    export let label      :string = "Select Date Range"
    export let start_date :string = new Date().toISOString().slice(0, 10)
    export let end_date   :string = new Date().toISOString().slice(0, 10)
</script>

<div>
<div>{label}</div>
    <input type="date" name="start_date" bind:value="{start_date}"  max="{end_date}"   />
    <input type="date" name="end_date"   bind:value="{end_date}"    min="{start_date}" />
</div>

<style></style>