<script  lang="ts">
    import { onMount }      from 'svelte'

    export let  path_connect: any
    export let  is_debug

    let path_str: string = ''

    function path( p: any ){                
        path_str = `M ${p.x0}, ${p.y0} C 
                ${(p.x1 - p.x0) / 2 + 15 + p.x0}, ${p.y0}
                ${(p.x1 - p.x0) / 2 - 15 + p.x0}, ${p.y1}
                ${p.x1}, ${p.y1}
            `  
    } 

    onMount(async () => { path(path_connect) })
</script>

{#if (path_str !== '')}
    <path id="bind_to_cursor" class="path-normal " d="{path_str}" />

    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <rect class="drag_area{is_debug ? '_debug': ''}" style="fill: lightsalmon;" 
        onpointermove = "{(e: any) => {
            path_connect.x1 = e.layerX
            path_connect.y1 = e.layerY

            path(path_connect)

            e.stopImmediatePropagation()
        }}"
        
        onpointerup = "{(e: any) => {  
            path_connect.enabled = false

            e.stopImmediatePropagation()
        }}"
    />
{/if}

<style>
    #bind_to_cursor  { stroke-width: 3; stroke: rgb(60, 60, 60); stroke-opacity: 1; fill-opacity:   0; filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4)); }
</style>