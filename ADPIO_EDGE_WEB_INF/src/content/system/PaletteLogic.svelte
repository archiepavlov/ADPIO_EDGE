<script lang="ts">
    import { 
        async_post,
    } from "../../stores";

    import { 
        USER_PROFILES,
    } from "../../app_engine";


    import {
        ExpandAll  ,
        CollapseAll,
        BuildImage,
        Information
    } from "carbon-icons-svelte"

    import { onMount }      from 'svelte'

    import DataTableEdit from "../../adp_components/components/DataTableEdit.svelte"
    import Modal         from "../../adp_components/components/Modal.svelte"
    import ControlPanel from "../../adp_components/components/ControlPanel.svelte"
    
    
    let datatable       : any = undefined
    let data = {
        header: "",
        colums: [
            {name: "ID",           key: "id"   ,        row_style: ""}, 
            {name: "NAME",         key: "name"     ,    row_style: ""},
            {name: "DESCRIPTION",  key: "description" , row_style: ""},
        ],
        groups: [
            {name: 'No Group', expand: true}
        ],        
        data: [],
    }
    let selected_el     : any = undefined

    let buttons:any = []

    function update_buttons(){
        return [ {
                text                : 'Collapse All',
                color               : 'normal',
                icon                : CollapseAll,

                onclick             : (e: any) => { datatable.collapse_all() }
            }, 

            {
                text                : 'Expand All',
                color               : 'normal',
                icon                : ExpandAll,

                onclick             : (e: any) => {  datatable.expand_all() }
            },         

            {
                text                : "Show Element's Info",
                color               : 'normal',
                icon                : Information,
                disabled            : selected_el.length === 0,

                onclick             : (e: any) => { 
                    selected_el = selected_el 
                    info_modal.open(120, 120)  
                }
            },         

            {
                text                : 'Rebuild Database',
                color               : 'red',
                icon                : BuildImage,

                with_confirmation   : true,
                conf_title          : "Are you sure you want to rebuild database?",  
                conf_description    : 'Some data may be lost during this action.',
                conf_btn_accept_txt : 'RERBUILD',

                onclick             : async (e: any) => { 
                    data.data = await async_post( '/system_tools', 'rebuild_logic_db' )  
                    datatable.update_groups()
                }
            },         
        ]
    }

    let info_modal      : any = undefined

    async function update_data(){
        data.data = await async_post( '/system_tools', 'update_logic' )
        datatable.update_groups()    
    }

    onMount(async () => { 
        update_data() 
        buttons = update_buttons()
    })    
</script>


<div class="content-panel">
    <ControlPanel buttons={buttons} />
</div>

<div class="content-panel">
    <DataTableEdit bind:this={datatable} data={data} context_btns={buttons}  group="group" 
       bind:selected_rows={selected_el}

        onselect={(e: any) => {
            buttons = update_buttons()
        }}       
    />
</div>


<Modal bind:this={info_modal} title="Info: { selected_el.length > 0? selected_el[0].name: '' }" > 
    {#if selected_el.length > 0}
        <div>
            <div class="flex-item">Type:        {selected_el[0].type}               </div>
            <div class="flex-item">Description: {selected_el[0].description}        </div>
            <div class="flex-item">Function:    {selected_el[0].function}           </div>
            <div class="flex-item">Lib Import:  {selected_el[0].libimport}          </div>
            <div class="flex-item">IO:          </div>

            {#each selected_el[0].io as rec}
                <div class="flex-item">{JSON.stringify(rec)} </div>
            {/each}

        </div>
    {/if}
</Modal>



<style>

</style>


