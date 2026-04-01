<script  lang="ts">
    import { 
      random_id
    } from "../../stores"

    export let label:string = ""
    export let value:string

    export let readonly:  boolean = false
    export let minlength: number  = 0
    export let maxlength: number  = 24 
    
    export let oninput   = function(e: any){}
    export let onkeydown = function(e: any){}

    export let width: number = 240
    const r_id = random_id()


    let this_input: any
    export function set_focus(){
        this_input.focus()
    }
</script>

<div style="width: {width}px;">
    <span class="input-container {readonly? 'input-container-readonly' : ''}">
        {#if readonly}
            <input inputmode="text" id="input-text-{r_id}" required
                onkeydown ={(e:any) => { e.preventDefault() }}
                oninput   ={(e:any) => { e.preventDefault() }}

                value={value} 
            >
        {:else}
            <input bind:this={this_input} inputmode="text" id="input-text-{r_id}" required 
                minlength  = {minlength}
                maxlength  = {maxlength}
                
                oninput   = {(e:any) => { oninput(e) }}
                onkeydown = {(e:any) => { onkeydown(e) }}

                bind:value={value}

            >
        {/if}


        <label for="input-text-{r_id}" class="input-label">{label}</label>
        <span  class="input-underline"></span>
    </span>
</div>

<style>

</style>