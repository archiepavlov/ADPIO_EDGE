<script  lang="ts">
import { 
  random_id
} from "../../stores"


export let label: string = ""
export let item_list:any = [
    {name: "Item 1", value: "Value1"},
]

export let readonly :boolean = false
export let value    :any

export let width    :number = 240

export let onchange = (e: any) => {}

const r_id:string = random_id()

</script>

<div style="width: {width}px;">
    {#if label !== "" }
        <label for="dropdown_{r_id}" class="dropdown-label">{label}</label>    
    {/if}

    {#if readonly}
        {#each item_list as item}
            {#if value === item.value}
                <span>{item.name} </span> 
            {/if}
        {/each}
    {:else}

        <select id="dropdown_{r_id}" class="dropdown-input"   bind:value="{value}" 
            onchange={(e:any) => {
                onchange(e)
            }}
        >
            {#each item_list as item}
                <option selected={value === item.value? true : false} value="{item.value}">
                    {item.name}
                </option>
            {/each}
        </select>    
    {/if}


</div>

<style>
    .dropdown-input {
        font-size: 0.92em;
        width: 100%;
        border: none;
        border-bottom: 2px solid #ff9800;
        /*padding: 5px 0;*/
        background-color: transparent;
        outline: none;
    }

    .dropdown-label {
        font-size: smaller;
        color: #9b9b9b;
        padding-top: 2px;
        padding-right: 8px;    
    }
</style>