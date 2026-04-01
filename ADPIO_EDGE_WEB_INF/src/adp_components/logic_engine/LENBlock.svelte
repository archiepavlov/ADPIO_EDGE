<script  lang="ts">
    export let content  : any
    export let selected : any
    export let selected_binds : any

    export let block   : any

    export let user: any
    export let drag_event: boolean

    export let blk_width  : any
    export let blk_height : any

    export let on_flip_datapoint = async (block: any) => { }
    export let on_dblclick       = async (block: any) => { }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<g id="block_{block.id}" class="st-{block.type}" transform="translate({block.x}, {block.y})"  
    onpointerdown="{(e:any) => {
        if ((!e.ctrlKey) && (!selected.includes( block ))) {
            selected = []
            selected_binds  = []
        }

        if (selected.includes( block )) {
            if ((e.button === 0) && (e.ctrlKey)) {//Delete element only on left btn click
                selected.splice( selected.indexOf(block), 1 )
            }
        } else { selected.push(block) } 

        selected.forEach((el: any) => {
            el.dX = el.x - e.layerX
            el.dY = el.y - e.layerY
            if (user.client === "firefox"){
                el.dX += - block.x
                el.dY += - block.y
            }
        })
        
        content = content
        e.stopImmediatePropagation() //Stop Handlers on mother's elements
    }}" 
               
    onpointermove  = "{(e: any) => { 
        if ((e.buttons > 0) && (selected.length > 0)) {  //Start Drag Event
            drag_event = true 
            e.stopImmediatePropagation()
        }
    }}"

    ondblclick = {(e: any) => { on_dblclick(e) }}
>

{#if block.type === 'datapoint-get'}
    <path class="{selected.includes(block)? 'selected' : ''}" d="M 0,10 L 0,30 {blk_width - 10},30 {blk_width},20 {blk_width - 10},10 Z" />
    <text class="st-block-caption" text-anchor="start" x="{20}" y="25" >{block.name}</text>
    <image class="cursor_pointer" onpointerdown="{async (e:any) => { await on_flip_datapoint(block) }}" x="{2}"  y="{12}" width="16" height="16" xlink:href="/resources/icons/setter.svg" /> 
{:else if block.type === 'datapoint-set'}
    <path class="{selected.includes(block)? 'selected' : ''}" d="M 0,20 L 10,30 {blk_width},30 {blk_width},10 10,10 Z" />
    <text class="st-block-caption" text-anchor="start" x="{10}" y="25"  >{block.name}</text> 
    <image class="cursor_pointer" onpointerdown="{async (e:any) => { await on_flip_datapoint(block) }}" x="{blk_width - 18}"  y="{12}"  width="16" height="16" xlink:href="/resources/icons/getter.svg" />      
{:else if block.type === 'constant'}
    <path class="{selected.includes(block)? 'selected' : ''}" d="M 0,10 L 0,30 {blk_width - 10},30 {blk_width},20 {blk_width - 10},10 Z" />
    <text class="st-block-caption no_event" text-anchor="start" x="4" y="25" >{block.io[0].value}</text>
{:else}<!--Normal Block-->
    <rect class="{selected.includes(block)? 'selected' : ''}" width="{blk_width}" height="{blk_height + block.io.length * 20}" />
    <text class="st-block-caption no_event" text-anchor="middle" x="{blk_width / 2}" y="20" >{block.name}</text>    
{/if}
    
</g>

<style>
    .selected { 
        stroke: deepskyblue !important; stroke-width: 4 !important; stroke-linecap: round !important; 
        rx: 5px !important; ry: 5px !important
    }

    /* Func block */ 
    .st-block rect:first-of-type { 
        fill: rgb(255, 255, 255); cursor: grab; stroke: slategrey; stroke-width: 2; stroke-linecap: round; 
        filter: drop-shadow(4px 4px 2px rgba(0, 0, 0, 0.4));
        rx:5px; ry:5px;
    }
    .st-block-caption        { font: inherit; font-size: 0.96em; }
    .st-block-description    { font: inherit; font-size: 1.0em; }  

    /*Custom  Blocks*/
    .st-datapoint-get        { filter: drop-shadow(4px 4px 2px rgba(0, 0, 0, 0.4)); }
    .st-datapoint-set        { filter: drop-shadow(4px 4px 2px rgba(0, 0, 0, 0.4)); }
    .st-constant             { filter: drop-shadow(4px 4px 2px rgba(0, 0, 0, 0.4)); } 

    .st-datapoint-set path   {  fill: lightsalmon;  stroke: slategrey; stroke-width: 2; stroke-linecap: round; }
    .st-datapoint-get path   {  fill: lightgreen;   stroke: slategrey; stroke-width: 2; stroke-linecap: round; }
    .st-constant path        {  fill: lightcyan;    stroke: slategrey; stroke-width: 2; stroke-linecap: round; }

</style>