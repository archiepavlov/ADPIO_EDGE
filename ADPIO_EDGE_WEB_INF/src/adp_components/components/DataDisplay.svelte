<script  lang="ts">
    import InputSwitch from "./InputSwitch.svelte"
    import InputNumber from "./InputNumber.svelte"
    import InputLabel  from "./InputLabel.svelte";


    export let readonly   : boolean = true
    export let datapoint  : any
    export let label      : string = ''

    export let onchange = function(e: any){}
</script>

{#if datapoint === undefined}
    UNDEFINED
{:else}

    {#if readonly}
        {#if datapoint.datatype === "bool"}
            {#if datapoint.value}
                {datapoint.properties.text_true} 
            {:else}
                {datapoint.properties.text_false}
            {/if}
        {:else if datapoint.datatype === "int"}
            {parseInt(datapoint.value)}
        {:else if datapoint.datatype === "float"}
            {parseFloat(datapoint.value).toFixed(datapoint.properties.decimals)} 
        {:else if datapoint.datatype === "str"}
            {datapoint.value}
        {:else}
            {datapoint.value} (Unknown type)
        {/if}
    {:else}
        {#if datapoint.datatype === "bool"}
            <InputSwitch label="{label}"    bind:value={datapoint.value}  
                text_false={datapoint.properties.text_false} text_true={datapoint.properties.text_true}
                onchange={(e:any) => { onchange(e) }}
            />   
        {:else if datapoint.datatype === "int"}
            <InputNumber label="{label}"    bind:value={datapoint.value} minvalue={datapoint.properties.min} maxvalue={datapoint.properties.max} 
                step={datapoint.properties.step}  type="int"
                onchange={(e:any) => { onchange(e) }}
            />
        {:else if datapoint.datatype === "float"}
            <InputNumber label="{label}"    bind:value={datapoint.value} minvalue={datapoint.properties.min} maxvalue={datapoint.properties.max} 
                step={datapoint.properties.step} type="float" decimals={datapoint.properties.decimals}
                onchange={(e:any) => { onchange(e) }}
            />
        {:else if datapoint.datatype === "str"}
            <InputLabel   label="{label}"    bind:value={datapoint.value} minlength={datapoint.properties.minlength} maxlength={datapoint.properties.maxlength} 
                oninput={(e:any) => { onchange(e) }}
            />
        {:else if datapoint.datatype === "≠"} 
            <div style="color: red">Mismatch of datatypes</div>
        {:else}
            <InputLabel label="Value"   bind:value="{datapoint.value}" 
                oninput={(e:any) => { onchange(e) }}
            />
            <div style="color: red">Type Does Not Exists: {datapoint.datatype}</div>
        {/if}

    {/if}
{/if}


<style>

</style>

