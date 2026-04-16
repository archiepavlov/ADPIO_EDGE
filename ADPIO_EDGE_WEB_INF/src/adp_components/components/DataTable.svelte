<script  lang="ts">
    import ContextMenu      from "./ContextMenu.svelte"
    import SignalPanel      from "./SignalPanel.svelte"

    export let data:any = {
        header: "Name Of the Table",
        colums: [
            {name: "User",        key: "user", row_style: ""},
            {name: "Profile",     key: "prof", row_style: ""},
            {name: "Description", key: "desc", row_style: ""}
        ],
        data: [
            {
                user_name_value  :   "name",
                profile_value    :   "profile",
                description_value:   "description",
            }
        ],
    }

    export let selectable_rows: boolean = false
    export let fill_height    : boolean = true
    export let selected_row: any = undefined
    export let onselect   = (e: any) => {}
    export let ondblclick = (e: any) => {}

    export let context_btns:any = []
    
    let context:any
</script>


{#if context_btns.length > 0}
    <ContextMenu buttons={context_btns} bind:this={context}   /> 
{/if}



<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="datatable {fill_height? 'auto_height' : 'auto_height_auto'}"           
    oncontextmenu="{(e: any) => {
        if ( context_btns.length === 0 ) return
        console.log(e)
        context.open_context(e.clientX, e.clientY)
        e.preventDefault()
    }}"
>
    {#if data.header !== ''}
        <div class="content-panel-header">{data.header}</div>
    {/if}

    <table>
        <thead>
            <tr>
                {#each data.colums as col}
                    <th style="{col.row_style}"><span>{col.name}</span></th>
                {/each}
            </tr>
        </thead>

        <tbody >
            {#each data.data as row}
                <tr class="{ selected_row === row? 'row_selected' : '' }">
                    {#each data.colums as col}
                        <td 
                            ondblclick="{(e: any) =>{ 
                                if (selectable_rows) {
                                    selected_row = row  
                                    ondblclick(e) 
                                }
                            }}"

                            onmousedown="{(e: any) => {
                                if (selectable_rows) {
                                    selected_row = row  
                                    onselect(e)
                                }         
                        }}" >
                            {#if col.key === 'panel'}
                                <SignalPanel dash={row[col.key]} />
                            {:else}
                                <span>{row[col.key]}</span>
                            {/if}
                        </td>                    
                    {/each}
                </tr>
            {/each}

        </tbody>
    </table> 
</div>

<style>
</style>