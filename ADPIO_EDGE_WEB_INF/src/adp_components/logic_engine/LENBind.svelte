<script  lang="ts">
    export let content  : any
    export let selected : any
    export let selected_binds : any

    export let  block   : any
    export let  io      : any

    export let  blk_width  : any
    export let  blk_height : any

    export let debug: boolean
    
    let bind_render: any = { x: 0, y: 0 }
    let path_d: string = ''

    function path( block: any, io: any ){
        let pointer_blk = content[io.bind.pointer_blk_index]
        const  blk_height_offst = (block.type !== 'block'       ? -20 : 0)
        const  pnt_height_offst = (pointer_blk.type !== 'block' ? -20 : 0)        

        bind_render = { 
            x: (pointer_blk.x + blk_width + 6), 
            y: (pointer_blk.y + blk_height + io.bind.pointer_io_index * 20 - 6 + pnt_height_offst)
        }
        
        path_d = `M ${(pointer_blk.x + blk_width + 3)}, ${(pointer_blk.y + blk_height + io.bind.pointer_io_index * 20 + 1 + pnt_height_offst)} C 
                ${((block.x - 3) - (pointer_blk.x + blk_width + 3))/2 + 15 + (pointer_blk.x + blk_width + 3)}, ${(pointer_blk.y + blk_height + io.bind.pointer_io_index * 20 + 1 + pnt_height_offst)}
                ${((block.x - 3) - (pointer_blk.x + blk_width + 3))/2 - 15 + (pointer_blk.x + blk_width + 3)}, ${(block.y       + blk_height + io.bind.this_io_index * 20    + 1 + blk_height_offst)}
                ${(block.x - 3)}, ${(block.y + blk_height + io.bind.this_io_index * 20 + 1 + blk_height_offst)}
            `  
        
        return path_d
    }    
</script>

<path class="path-normal" d="{ path( block, io ) }" />

<!-- svelte-ignore a11y_no_static_element_interactions -->
<path class="{ selected_binds.includes( io ) ? 'path-selected' : 'path-area' }" 
    onpointerdown="{(e:any) => { 
        if (!e.ctrlKey) {
            selected        = []
            selected_binds  = []
        }
        selected_binds.push(io) 
        e.stopImmediatePropagation()
    }}"

    d="{ path_d }" 
/>


{#if debug && ('debug_value' in content[io.bind.pointer_blk_index].io[io.bind.pointer_io_index])} 
    <text text-anchor="start"   class="bind-value "  x="{bind_render.x}"  y="{bind_render.y}" >
        '{content[io.bind.pointer_blk_index].io[io.bind.pointer_io_index].debug_value}'
    </text>
{/if}


<style>

    /* Paths */
    .path-normal            { stroke-width: 3; stroke: rgb(60, 60, 60); stroke-opacity: 1; fill-opacity:   0; filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4));}

    .path-area              { stroke-width: 8; fill: none; stroke: red;  stroke-opacity: 0.0; }
    .path-area:hover        { stroke-width: 8; fill: none; stroke: rgb(172, 172, 172);  stroke-opacity: 1; cursor: grab;  }
    
    .path-selected          { stroke-width: 6; fill: none; stroke: deepskyblue }    

    .bind-value             {  font: inherit; font-size: 0.92em; }
</style>