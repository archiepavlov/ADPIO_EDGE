<script  lang="ts">
    let  box_mode   : any = {enabled: false, x0: 0, x1: 0, y0: 0, y1: 0}

    export let  content    : any
    export let  selection   : any

    export let  blk_width  : any
    export let  blk_height : any

    export function on_start_box(event: any){
        box_mode.enabled = true
        box_mode.x0      = event.layerX
        box_mode.x1      = event.layerX
        box_mode.y0      = event.layerY 
        box_mode.y1      = event.layerY        
    }

    export function on_stop_box(event: any){
        if (box_mode.enabled) box_selector() 
        box_mode.enabled = false        
    }

    export function on_move_box(event: any){
        if ((event.buttons > 0) && box_mode.enabled) { //BOX mode
                box_mode.x1      = event.layerX
                box_mode.y1      = event.layerY
            }        
    }

    function box_selector(){
        const bx = [Math.min( box_mode.x0, box_mode.x1), Math.max(box_mode.x0, box_mode.x1), Math.min( box_mode.y0, box_mode.y1),  Math.max(box_mode.y0, box_mode.y1)]
        
        content.forEach((el: any) => {
            if ((bx[0] < el.x) && (bx[0] < (el.x + blk_width)) && (el.x < bx[1]) && ((el.x + blk_width) < bx[1]))
                if ((bx[2] < el.y) && (bx[2] < (el.y + blk_height)) && (el.y < bx[3]) && ((el.y + blk_height) < bx[3]))
                    if (!selection.includes(el))
                        selection.push(el)
        })
    }    
</script>

{#if box_mode.enabled}
    <g id="box_selector">
        <rect class="drag_area" />
        <path d="M {box_mode.x0},{box_mode.y0} L {box_mode.x0},{box_mode.y1} {box_mode.x1},{box_mode.y1} {box_mode.x1},{box_mode.y0} Z" stroke="black" fill="transparent" />
    </g>
{/if}

<style>
   
</style>