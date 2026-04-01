<script  lang="ts">
    import { onMount, onDestroy }      from 'svelte'

    import { debug }       from '../../../package.json';
    import Modal           from '../../adp_components/components/Modal.svelte'

    export let data: any
    export let data_r: any = []

    let trend_widget : any = undefined

    let dp_info_modal: any = undefined
    let dp_selected  : any = undefined
    

    const is_debug = debug

    let cnv: any = { 
        renderd: false,
        width: 1040, height: 460,        //Canvas dimentions and 
        
        pad_top:    60, pad_bottom: 40,
        pad_left:   60, pad_right:  60,

        line: "M 0,0 L 0,0 Z",           //Lines

        y_marks   : [],      //Marks Y
     
        x_marks_line_t : [], //Marks X Time
        x_marks_line_d : [], //Marks X Date
    }


    async function update_canvas(){
        cnv.renderd = false
        if (trend_widget === undefined) return
        cnv.width   = trend_widget.scrollWidth
        if (cnv.width < 620) cnv.width = 620

        if (data.length < 2) return
        data_r = JSON.parse( JSON.stringify( data ) ).reverse() //Remember, List loads in reverse!

//Y-Axis  y_marks format {x: 40, y: 120, value: 'value'}    
        cnv.y_marks = []    
        let y_auto_min = data_r[0].value
        let y_auto_max = data_r[0].value
        data_r.forEach((el: any, index: number) => {
            if (el.value < y_auto_min) y_auto_min = el.value
            if (el.value > y_auto_max) y_auto_max = el.value
        })
 
        const marks_y   = 6
        const y_step_u  = ( y_auto_max - y_auto_min ) / marks_y                     //Step in units
        const y_step_px = ( cnv.height - cnv.pad_top - cnv.pad_bottom  ) / marks_y  //Step in pixels
           
        //console.log(y_step_u)

        for (let i = 0; i <= marks_y; i ++) {
            //Make Here scaling to work
            //console.log('FIX SCALING BY Y AXIS (ROUND)')
            cnv.y_marks.push({
                x: cnv.pad_left, 
                y: (cnv.height - cnv.pad_bottom) - y_step_px * i,  
                value: (y_auto_min   + y_step_u * i).toFixed(2)
            })
        }


//X-Axis  x_marks format {x: 40, y: 120, value: 'value'}    
        cnv.x_marks_line_t = [] 
        cnv.x_marks_line_d = []
        let x_auto_min = data_r[0].epoch 
        let x_auto_max = data_r[data_r.length - 1].epoch

        const x_step_px = ( cnv.width  - cnv.pad_left - cnv.pad_right ) / ( x_auto_max - x_auto_min ) //Epoch per pix

//X-Date Only            
        let date_buf:string     = ''        //Make Sure to mark only new day only
        let date_old_pos:number = -999

//X-Time Only             
        const time_min_dist     = 80        //Monitor Minimum possible time stamps dist
        let time_old_pos:number = -999

        data_r.forEach((el: any, index: number) => {
            const new_x_coord =  ( el.epoch - x_auto_min ) * x_step_px + cnv.pad_left

            //DATE
            if ((date_buf !== el.date) && (new_x_coord >= (date_old_pos + time_min_dist))){
                date_buf     = el.date
                date_old_pos = new_x_coord //Save current coord
                cnv.x_marks_line_d.push({
                    x: new_x_coord, 
                    y: 42, 
                    value: el.date
                } )
            }

            //TIME
            if (new_x_coord >= (time_old_pos + time_min_dist)){
                time_old_pos = new_x_coord //Save current coord
                cnv.x_marks_line_t.push({
                    x: new_x_coord, 
                    y: cnv.height - 20, 
                    value: el.time
                } )
            }
        })

//DATAPOINTS
        const val_step_u  = (cnv.height - cnv.pad_bottom - cnv.pad_top) / ( y_auto_max - y_auto_min ) //Pixel per unit
        data_r.forEach((el: any, index: number) => {
            el.x = cnv.pad_left + ( el.epoch - x_auto_min ) * x_step_px
            el.y = cnv.height - cnv.pad_bottom - val_step_u * ( el.value - y_auto_min )

            if (index === 0)
                cnv.line = `M ${el.x},${el.y} L `
            else 
                cnv.line += `${el.x},${el.y} `                
        })

        cnv.renderd = true
    }

    onMount(async () => { 
        //await sleep(250)
        await update_canvas()
    })

    onDestroy(async () => {  })
</script>

<svelte:window onresize="{() => { 
    if (trend_widget !== undefined) update_canvas()  
}}" />

<div  id="time_trend" bind:this={trend_widget}  >
{#if cnv.renderd}
    <svg id="time_trend_svg" class="{is_debug ? 'time_trend_svg_debug' : ''}" width="{cnv.width}" height="{cnv.height}" xmlns="http://www.w3.org/2000/svg">

    <!-- Labels X --> 
        {#each cnv.x_marks_line_t as mk }
            <text x="{mk.x}" y="{mk.y}"  class="label_xt">{mk.value}</text>

            {#if is_debug}
                <line class="axisXT" 
                    x1="{mk.x}" y1="{cnv.pad_top}" 
                    x2="{mk.x}" y2="{cnv.height - cnv.pad_bottom}"  
                />
            {/if}     
        {/each}

        {#each cnv.x_marks_line_d as mk }
            <text class="label_xd"  transform=" translate({mk.x},{mk.y}) rotate(-12)">
                {mk.value}
            </text>

            <line class="axisXD" 
                x1="{mk.x}" y1="{cnv.pad_top}" 
                x2="{mk.x}" y2="{cnv.height - cnv.pad_bottom}"  
            />
        {/each}

    <!-- Labels Y -->
        {#each cnv.y_marks as mk }
            <text x="{mk.x - 4}" y="{mk.y + 6}"  class="label_y">{mk.value}</text>

            {#if is_debug}
                <line class="axisY" 
                    x1="{cnv.pad_left}"               y1="{mk.y}" 
                    x2="{cnv.width - cnv.pad_right }" y2="{mk.y}"  
                />
            {/if}   
        {/each}   
        
        
    <!--Axis-->
        <line id="axisX" class="axis_xy"
            x1="{cnv.pad_left}"                  y1="{cnv.height - cnv.pad_bottom}" 
            x2="{cnv.width - cnv.pad_right + 6}" y2="{cnv.height - cnv.pad_bottom}" 
        />1

        <line id="axisY"  class="axis_xy"
            x1="{cnv.pad_left}" y1="{cnv.pad_top - 6}" 
            x2="{cnv.pad_left}" y2="{cnv.height - cnv.pad_bottom}"  
        />
                      
    <!--Path  -->   
        <path class="line_std"  d="{cnv.line}"/>

    <!--Draw Points -->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        {#each data_r as d_rec }
            <circle class="dp_normal {dp_selected === d_rec? 'dp_selected': ''}" cx="{d_rec.x}" cy="{d_rec.y}" 
            onclick={() => { 
                dp_selected = d_rec
                dp_info_modal.open(240, 120)
            }} />
        {/each}

    </svg>   
{/if}       
</div>

<Modal bind:this={dp_info_modal} title="Datapoint Record Info" >
    {#if dp_selected !== undefined}
        <div class="flex flex-col">
            <div class="flex-item ">Value: {dp_selected.value}</div>
            <div class="flex-item ">Time:  {dp_selected.time}</div>
            <div class="flex-item ">Date:  {dp_selected.date}</div>
        </div>    
    {/if}
</Modal>



<style>
    #time_trend { /*border: 1px solid grey;*/  width: 100%; /* height: calc(100vh - 160px); */ overflow: auto; }

    #time_trend_svg{
        position: relative;
        background-color: transparent;

        width: 100%;
        min-width: 620px;
    }

    .time_trend_svg_debug{
        background-image: linear-gradient(rgb(220, 220, 220) 1px, transparent 1px), linear-gradient(to right, rgb(250, 250, 250) 1px, transparent 1px);
        background-size: 20px 20px;      

        background-position-x: 20px;
        background-position-y: 20px; 

        /*
            https://10015.io/tools/css-background-pattern-generator
            fill="{selected_elements.includes(block) ? 'lightblue' : 'white'}"
        */        
    }

    /* AXIS AND LABELS */
    .axis_xy{
        stroke: #666;   
        stroke-width: 3;
        stroke-linecap: round;
    }


    .label_xt { 
        font: inherit;
        fill: #828282;
        text-anchor: middle;
    }

    .label_xd { 
        font: inherit; 
        fill: #646464;
        text-anchor: middle;
    }

    .label_y { 
        font: inherit; 
        fill: #646464;
        text-anchor: end;
    }

/* Datapoints and line */
    .line_std {
        fill  : transparent;
        stroke: #646464;
    }

    .dp_normal {
        fill: #646464;
        cursor: crosshair;
        r: 3px;
        stroke: transparent;
        stroke-width: 7px;
    }

    .dp_selected {
        fill: #00bfff !important;
    }

    .axisXD   { stroke:rgb(255, 176, 73);    stroke-width: 1; }    

/* Debug */
    .axisXT   { stroke:lightseagreen; stroke-width: 1; }
    .axisY    { stroke:orange;        stroke-width: 1; }
</style>