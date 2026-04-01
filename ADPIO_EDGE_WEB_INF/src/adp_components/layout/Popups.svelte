<script  lang="ts">
//https://uiverse.io/seyed-mohsen-mousavi/heavy-cobra-18

import {
    Warning ,
    Close,
} from "carbon-icons-svelte"

import { 
    popup_list,
    popup_delete,
} from "../../stores";

$: pops      = $popup_list

</script>

{#each pops as pop}
    <div class="popup" style="top: {60 + pops.indexOf(pop) * 60}px;">
        <div class="flex flex-row ">
            <div class="popup-svg">
                <Warning size={24} />
            </div>
            
            <div class="popup-text flex-fill">
                <div>{pop.header}</div>
                <div>{pop.description}</div>
            </div>
            
            <button class="popup-close" onclick="{() => { popup_delete(pops.indexOf(pop)) }}"> 
                <Close size={24} />
            </button>

        </div>
    </div>
{/each}
    



<style>
    .popup{
        background-color: rgb(35 37 49);

        border-radius: 5px;
        width: 380px;

        position: fixed;
        right: 10px;
        z-index: 9999;

        & > div {
            padding-left: 5px;
            padding-right: 5px;
        }
    }

    .popup-svg{
        color: rgb(214 85 99);
        transform: translateY(40%);
    }

    .popup-text{
        font-size: smaller;
        color: whitesmoke;
        padding: 6px;
        width: min-content;
    }

    .popup-close{
        color: rgb(184, 184, 184);
        transform: translateY(40%);

        border-radius: 3px;
        transition: all 0.25s;  

        height: 28px;
        width:  28px;
        text-align: center;

        &:hover{
            color: rgb(214 85 99);
        }
    }
</style>