<script  lang="ts">
    import { 
      random_id
    } from "../../stores"

    export let label = "PASSWORD"
    export let value:string

    export let minlength: number  = 0
    export let maxlength: number  = 16 

    export let oninput = function(e: any){}
    export let onkeydown = function(e: any){}
    
    export let width: number = 240
    const r_id = random_id()


    let this_input: any
    export function set_focus(){
        this_input.focus()
    }

</script>

<div style="width: {width}px;">
    <span class="input-container">
        <input bind:this={this_input} type="password" id="input-text-password-{r_id}" required
            
            minlength  = {minlength}
            maxlength  = {maxlength}

            oninput   = {(e:any) => { oninput(e) }}
            onkeydown = {(e:any) => { onkeydown(e) }}
            
            bind:value={value}
        >

        <label for="input-text-password-{r_id}" class="input-label">{label}</label>
        <span  class="input-underline"></span>
    </span>
</div>

<style>

</style>