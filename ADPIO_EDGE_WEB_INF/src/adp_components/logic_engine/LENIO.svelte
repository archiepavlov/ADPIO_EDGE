<script  lang="ts">
    import { 
        popup_add,
    } from "../../stores" 

    export let  block       : any
    export let  io          : any
    export let  io_index    : any

    export let  path_connect: any
    

    export let  blk_width  : any
    export let  blk_height : any

    export let on_bind = async (e: any) => {}
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<g transform="translate( 
    { io.type === "input" 
        ? (block.x - 2)                                             
        : (block.x + blk_width - 2) 
    }, 

    { io.type === "input" 
        ? (block.y + blk_height + io_index * 20 - 1 + (block.type !== 'block'? -20 : 0)) 
        : (block.y + blk_height + io_index * 20 - 2 + (block.type !== 'block'? -20 : 0))   
    }
)"

    onpointerdown="{(e:any) => {
        path_connect.x0 = Math.round(e.offsetX / 20) * 20
        path_connect.y0 = Math.round(e.offsetY / 20) * 20 
        path_connect.x1 = path_connect.x0
        path_connect.y1 = path_connect.y0

        path_connect.bind0_block     = block
        path_connect.bind0_io        = io
        path_connect.bind0_io_index  = block.io.indexOf( io )

        path_connect.enabled = true
        e.stopImmediatePropagation()
    }}" 

    onpointermove = "{(e: any) => {
        e.stopImmediatePropagation()
    }}"

    onpointerup="{async (e:any) => {
        if (path_connect.enabled === false) return
        path_connect.enabled = false
        path_connect.bind1_block        = block
        path_connect.bind1_io           = io
        path_connect.bind1_io_index     = block.io.indexOf( io )

        if (io.bind.bind_id !== undefined){
            popup_add("ILLIGAL BIND", "Already Binded. Only one bind per input allowed")
            return                         
        }
        
        await on_bind(e)

        e.stopImmediatePropagation()
    }}"                
>
    {#if      io.type === "input"}                
        {#if block.type === 'block'}
            <text text-anchor="start" class="no_event"   x="{10}" y="{6}" >{io.name}</text>
        {/if}
        <circle class="block-input"   cx="{2}" cy="{2}" r="{3}" /> 
        <circle class="block-io-zone" cx="{2}" cy="{2}" r="{9}" /> 
    {:else if io.type === "output"} 
        {#if block.type === 'block'}
            <text text-anchor="end"   class="no_event"  x="{-8}"  y="{6}" >{io.name}</text>
        {/if}
        <rect class="block-output"    x="{0}"   y="{0}" width="{5}" height="{5}" />
        <circle class="block-io-zone" cx="{2}" cy="{2}" r="{9}" /> 
    {/if}   
   
</g>

<style>
    /* IO Zone*/
    .block-io-zone          { cursor: crosshair;  fill-opacity: 0.0;  fill: rgb(0, 35, 150); }
    .block-input            { stroke: rgb(60, 60, 60); stroke-width: 1; fill: lightsalmon; }
    .block-output           { stroke: rgb(60, 60, 60); stroke-width: 1; fill: lightgreen; }  
</style>