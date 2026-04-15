<script lang="ts">
    import { onMount, onDestroy }      from 'svelte'

    import { 
        async_post,
    } from "../../stores"

    import DataTable        from "../../adp_components/components/DataTable.svelte"
    import Modal            from "../../adp_components/components/Modal.svelte"
    import ControlPanel     from "../../adp_components/components/ControlPanel.svelte"
    import ButtonR          from '../../adp_components/components/ButtonR.svelte'
    
    import {
        Edit,
        ConnectionSignal,
        DataQualityDefinition, 
        Run,
        Add,
        TrashCan,
        Folder,
        BuildImage,
        PlayOutline,
        StopOutline,
        Restart,
        Play,
        Stop,
        Save,
        ArrowsVertical,
        ArrowUp,
        ArrowDown,
        
        DataError,
        DataView,
        DataBackup
    } from "carbon-icons-svelte"
    

    let datatable           : any = undefined
    let selected_device     : any = undefined
    let selected_object     : any = undefined
    let view_objects_modal  : any = []
    
    let interval_update: number

    let data: any = {
        header: "",
        colums: [
            {name: "",                key: "panel",         row_style: "width: 120px;"}, 
            {name: "ID",              key: "id",            row_style: "", }, 
            {name: "DEVICE ID",       key: "device_id",     row_style: "", },    
            {name: "NETWORK",         key: "net",           row_style: "", }, 
            {name: "NAME",            key: "name",          row_style: "", }, 
            {name: "DESCRIPTION",     key: "description",   row_style: "", }, 
            {name: "LOCATION",        key: "location",      row_style: "", }, 

            //{name: "TX",        key: "segment_tx",      row_style: "", }, 
            //{name: "RX",        key: "segment_rx",      row_style: "", }, 
        ],       
        data: [],
    }

    let dev_data: any = {
        header: "",
        colums: [       
            /*{name: "",              key: "panel",        row_style: "width: 52px;"},      */
            {name: "OBJECT",    key: "object",  row_style: "width: 240px;", }, 
            {name: "NAME",      key: "name",    row_style: "width: 320px;", }, 
            {name: "VALUE",     key: "value",   row_style: "", }, 
        ],       
        data: [],
    }


    let buttons:any = []

    function update_buttons(){
        let btn:any = [
            /*{
                text                : 'Refresh',
                color               : 'normal',
                icon                : Run,
                disabled            : false,

                with_confirmation   : false,

                onclick             : async (e: any) => { await update() }
            },*/

            {
                text                : 'Read Object List',
                color               : 'normal',
                icon                : DataBackup,
                disabled            : selected_device === undefined,

                onclick             : async (e: any) => {
                    await read_object_list(selected_device)
                }
            }
        ]

        return btn
    }

    async function read_object_list(device: any){
        let request:any = []

        if (device.segment_tx){
            request.push({ 
                'cmd': 'read_device_list', 
                'params': {
                    'id'        : device.id,
                    'net'       : device.net, 
                    'object'    : `device, ${device.device_id}`, 
                    'property'  : 'objectList', 
                }
            })
        } else {
            for (let i = 1; i <= device.list_size; i++){ 
                request.push({ 
                    'cmd': 'read_device_list', 
                    'params': {
                        'id'        : device.id,
                        'net'       : device.net, 
                        'object'    : `device, ${device.device_id}`, 
                        'property'  : 'objectList', 
                        'index'     : i 
                    }
                })
            } 
        }

        await bacnet_command(request)        
    }

    async function read_object_short_info(device: any, object: any){
        let request:any = []

        if (object.name === "")
            request.push({ 
                'cmd': 'read_property_db', 
                'params': { 
                    'id'        : device.id, 
                    'net'       : device.net,  
                    'object_id' : object.object_id,               
                    'object'    : object.object,                 
                    'property'  : 'objectName',
                } 
            })

        request.push({ 
            'cmd': 'read_property_db', 
            'params': { 
                'id'        : device.id, 
                'net'       : device.net, 
                'object_id' : object.object_id,
                'object'    : object.object,                 
                'property'  : 'presentValue'
            } 
        })

        await bacnet_command(request)
    }

    async function read_object_short_info_all(device: any){
        let request:any = []

        device.objects.forEach((object: any) => {
            if (object.name === "")
                request.push({ 
                    'cmd': 'read_property_db', 
                    'params': { 
                        'id'        : device.id, 
                        'net'       : device.net,  
                        'object_id' : object.object_id,               
                        'object'    : object.object,                 
                        'property'  : 'objectName',
                    } 
                })

            request.push({ 
                'cmd': 'read_property_db', 
                'params': { 
                    'id'        : device.id, 
                    'net'       : device.net, 
                    'object_id' : object.object_id,
                    'object'    : object.object,                 
                    'property'  : 'presentValue'
                } 
            })            
        });

        await bacnet_command(request)
    }

    async function read_object_properties(){
        let request:any = []
        await bacnet_command(request)
    }

    async function bacnet_command(cmd: any){
        const read = await async_post( '/network_tools', 'bacnet_tools_read_properties', cmd )
        //console.log(read)
    }

    async function show_objects_modal(){
        if (selected_device.objects.length === 0)
            await read_object_list(selected_device)
        
        view_objects_modal.open(120, 120) 
        await update()
    }    

    async function update(){
        data.data = await async_post( '/network_tools', 'bacnet_tools_update' )
        //console.log(data.data)

        data.data.forEach((el: any) => {
            el.panel = []
            
            if (el.objects.length === 0)                 { el.panel.push({ icon: DataError,  color: "grey",   text: `Object List Not Read. Size: ${el.list_size}`}    ) } 
            else if (el.list_size === el.objects.length) { el.panel.push({ icon: DataView,   color: "green",  text: `Object List Read. Size: ${el.objects.length}`}   ) }
            else                                         { el.panel.push({ icon: DataBackup, color: "orange", text: `Progress: ${el.objects.length}/${el.list_size}`} ) } 

            if ((el.segment_rx) && (el.segment_tx)) { el.panel.push({ icon: ArrowsVertical,  color: "green", text: 'Segmentation TX and RX'}) } 
            else if (el.segment_tx)                 { el.panel.push({ icon: ArrowUp,         color: "green", text: 'Segmentation TX'}) } 
            else if (el.segment_rx)                 { el.panel.push({ icon: ArrowDown,       color: "green", text: 'Segmentation RX'}) } 
            else                                    { el.panel.push({ icon: ArrowsVertical,  color: "grey",  text: 'No Segmentation'}) }
        

            if ((selected_device !== undefined)&& (selected_device.net === el.net)) {
                dev_data.data = el.objects
                selected_device = el

                //console.log(dev_data)
            }           
        })   
    }

    onMount(async () => { 
        buttons = update_buttons()
        await update()
        interval_update = setInterval(async () => { await update() }, 2000)
    })

    onDestroy(async () => {
        clearInterval(interval_update)
    }) 

</script>


<div class="content-panel">
    <ControlPanel buttons={buttons} />
</div>

<div class="content-panel"> <!--group="group" -->
    <DataTable bind:this={datatable} data={data}  context_btns={buttons} bind:selected_row={selected_device}  selectable_rows={true}
        onselect={(e: any) => {
            buttons = update_buttons()         
        }}
        
        ondblclick={(e: any) => {
            show_objects_modal()
        }}
    />
</div>


{#if (selected_device !== undefined)}
    <Modal bind:this={view_objects_modal} title="{selected_device.device_id} [{selected_device.net}]: {selected_device.name}" >
        <div class="modal_panel">
            <ButtonR  icon={DataBackup}   text="Read All" color="normal" 
                onclick={async (e: any) => { 
                    await read_object_short_info_all(selected_device)
                }}
            />
        </div>         
        
        <div id="fields">
            <DataTable data={dev_data} selectable_rows={true} bind:selected_row={selected_object} fill_height={false} 
                onselect={async (e: any) => {
                    await read_object_short_info(selected_device, selected_object)
                }}
            />
        </div>
    </Modal>
{/if}


<style>

    #fields {
        width: 720px; 
        max-height: 420px;
        display: flex;
    }

    .modal_panel{
        padding: 5px;
    }

</style>

