<script  lang="ts">
    import { async_post } from "../../stores";

    import {
        Clean,
        Run,
    } from "carbon-icons-svelte"

    import { onMount } from 'svelte'

    import DataTable    from "../../adp_components/components/DataTable.svelte"
    import ControlPanel from "../../adp_components/components/ControlPanel.svelte"


    let data = {
        header: "",
        colums: [
            {name: "DATE",  key: 'date',  row_style: "width: 180px;"},
            {name: "TYPE",  key: 'type',  row_style: "width: 100px;"},
            {name: "TEXT",  key: 'text',  row_style: ""},
        ],
        data: []
    }


    let buttons:any = [
        {
            text                : 'Refresh',
            color               : 'normal',
            icon                : Run,
            disabled            : false,

            with_confirmation   : false,

            onclick             : async (e: any) => { await update_data() }
        }, 

        {
            text                : 'Clear All',
            color               : 'red',
            icon                : Clean,
            disabled            : false,

            with_confirmation   : true,
            conf_title          : 'Clear Logs',
            conf_description    : 'Are you sure you want to delete all records?',
            conf_btn_accept_txt : 'DELETE',            

            onclick             : async (e: any) => { 
                const res = await async_post( '/logger', 'clear_all' )
                data.data = []
            }
        }, 
    ]

    async function update_data(){
        data.data = await async_post( '/logger', 'update' )
    }

    onMount(async () => { update_data() })
</script>

<div class="content-panel">
    <ControlPanel buttons={buttons} />
</div>

<div class="content-panel">
   <DataTable data={data}  />
</div>


<style>

</style>