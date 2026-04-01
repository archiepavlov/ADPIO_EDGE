<script  lang="ts">
    import { onMount, onDestroy }      from 'svelte'
    
    import { 
        async_post,
    } from "../../stores"

    import Modal            from '../../adp_components/components/Modal.svelte'
    import ButtonR          from '../../adp_components/components/ButtonR.svelte'
    import InputSelector    from '../../adp_components/components/InputSelector.svelte'
    import DataTable        from '../../adp_components/components/DataTable.svelte'
    import TETimeChart      from '../../adp_components/trend_engine/TETimeChart.svelte'
    import ControlPanel     from '../../adp_components/components/ControlPanel.svelte'
    import DatePicker       from '../../adp_components/components/DatePicker.svelte'
    import InputSwitch      from '../../adp_components/components/InputSwitch.svelte'

    import {
        Add,
        ChartLineData,
        Table,
        GlobalLoanAndTrial
    } from "carbon-icons-svelte"


    const VIEW_GRAPH  = 0
    const VIEW_TABLE  = 1

    let view: number = VIEW_GRAPH

    let data = {
        header: "",
        colums: [
            {name: "DATE",   key: 'date',    row_style: "width: 160px;"},
            {name: "TIME",   key: 'time',    row_style: "width: 100px;"},
            {name: "VALUE",  key: 'value',   row_style: ""},
        ],
        data: []
    }

    let buttons   : any    = []

    let app_list  : any    = []
    let app_select: string = ''

    let dp_list   : any    = []  //app.trends
    let dp_select : string = ''

    let select_trend_modal  : any = undefined
    
    let date_range: boolean = false
    let start_date :string = new Date().toISOString().slice(0, 10)
    let end_date   :string = new Date().toISOString().slice(0, 10)


    function update_buttons(){ 
        let btns: any = [
            {
                text                : 'REFRESH',
                color               : 'green',
                icon                : Add,
                disabled            : false, //dp_list.length === 0,
            
                onclick             : async (e: any) => { 
                    /*await load_trend(app_select, dp_select)*/
                    select_trend_modal.open(120, 120)
                }
            },

           {
                text                : 'GRAPH VIEW',
                color               : 'normal',
                icon                : ChartLineData ,
                disabled            : (view === VIEW_GRAPH? true : false),

                onclick             : async (e: any) => { 
                    view    = VIEW_GRAPH
                    buttons = update_buttons()
                }
            },  

            {
                text                : 'TABLE VIEW',
                color               : 'normal',
                icon                : Table,
                disabled            : (view === VIEW_TABLE? true : false),

                onclick             : async (e: any) => { 
                    view    = VIEW_TABLE
                    buttons = update_buttons()
                }
            },
        ]
        return btns
    }

    async function load_trend(s_app: string, s_dp_name: string){
        if (date_range){
            data.data = await async_post( '/trends', 'load_date_range_trend', {app: s_app, datapoint: s_dp_name, start: start_date, end: end_date  } ) //load date range
        } else {
            data.data = await async_post( '/trends', 'load_last_trend',      {app: s_app, datapoint: s_dp_name} ) //load last 1200 records
        }
        
    }

    onMount(async () => { 
        view = VIEW_GRAPH

        app_list = await async_post( '/trends', 'get_trend_list' )
        buttons = update_buttons()
    })

    onDestroy(async () => {  })
</script>


<div class="content-panel">
    <ControlPanel buttons={buttons} />               
</div>

<div class="content-panel ">
    {#if dp_select.length === 0}
        <span>SELECT APP AND DATAPOINT TO DISPLAY</span>
    {:else if view === VIEW_GRAPH}
        {#key data.data}
            <TETimeChart data={data.data} />
        {/key}
    {:else if view === VIEW_TABLE}
        <DataTable data={data}  />
    {:else}
        <span>VIEW DOES NOT EXIST </span>
    {/if}
</div>


<Modal bind:this={select_trend_modal} title="Select Trend To Display" > 
    <div class="flex flex-col">
        <div class="flex-item "><InputSelector label="Select App" bind:value={ app_select } item_list={app_list}  
            onchange={(e: any)=>{ 
                dp_list = app_list.find((el: any) => app_select === el.value).trends
                buttons = update_buttons()
            }}
        /></div>

        <div class="flex-item "><InputSelector label="Select Datapoint" bind:value={ dp_select } item_list={dp_list}  readonly={dp_list.length === 0}
            onchange={async (e: any)=>{
                //await load_trend(app_select, dp_select)
                buttons = update_buttons()
            }}
        /></div>

        <div class="flex-item"><InputSwitch bind:value={date_range} label="Date Range" /></div>

        {#if date_range}
            <div class="flex-item">
                <DatePicker bind:start_date={start_date} bind:end_date={end_date} />
            </div>
        {/if}
        
        <div class="flex-item ">
            <ButtonR text="Save" color="green" icon={GlobalLoanAndTrial} disabled={dp_select === ""} onclick={async (e:any, ) =>  {
                await load_trend(app_select, dp_select)
            }} />
        </div>   
    </div>
</Modal>


<style>

</style>

