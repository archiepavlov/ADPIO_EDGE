<script lang="ts">
	import { user_params }     from "../../stores.js"
    import { version, debug }  from '../../../package.json';

    const info        = $user_params.client
    const get_version = version
    const get_debug   = debug
</script>


<div class="content-panel">
    <div class="content-panel-header">ADPIO EDGE</div>

    {#if get_debug}
        <div style="color: red;">Debug Version: {get_version}</div>
    {:else}
        <div>Build Version: {get_version}</div>
    {/if}

    <div style="margin-top: 15px;">By Artem Pavlov</div> 
    <div>Vacnouver, BC</div>
    <div>Canada</div>

    <div style="margin-top: 15px;"><a class="email_to" href="mailto:apavlov.adpautomation@gmail.com">Contact Email</a></div>
    <div style="margin-top: 25px;">Client: {info}</div>
</div>

<style>
    .email_to {
        color: cornflowerblue !important;
        text-decoration: underline !important;
    }
</style>