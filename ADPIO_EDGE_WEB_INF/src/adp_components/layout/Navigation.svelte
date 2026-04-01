<script  lang="ts">
    import {
        Search,
        Delete,
    } from "carbon-icons-svelte"   

    import {
        set_user_params,
        set_navigation
    } from "../../stores.js"

   
    import { debug, version }       from '../../../package.json'
    const get_debug   = debug
    const get_version = version

    export let user:any

    function filter_tree(filter: string){
        if (user.filter === "") {
            user.active_tree.forEach((top_lvlv:any) => {
                top_lvlv.visible = true

                top_lvlv.submenu.forEach((sec_lvlv:any) => { sec_lvlv.visible = true });
            });
        } else {
            user.active_tree.forEach((top_lvlv:any) => {
                let top_lvlv_is_visible = false
                top_lvlv.visible = false

                top_lvlv.submenu.forEach((sec_lvlv:any) => {
                    if (sec_lvlv.name.toLowerCase().includes(filter)){
                        sec_lvlv.visible = true 
                        top_lvlv_is_visible = true
                    } else {
                        sec_lvlv.visible = false 
                    }
                });

                if (top_lvlv_is_visible) top_lvlv.visible = true
            });
        }
    }


</script>


<div id="nav-search">
    <input id="search_navi" type="text" required  bind:value={user.filter} onkeyup="{() =>{
        set_user_params(user)
        filter_tree(user.filter.toLowerCase())
    }}" />

    <button id="nav-search-clear" onclick={()=>{ 
            user.filter = "" 
            filter_tree(user.filter)
            set_user_params(user)
        }} >
        <Delete  />
    </button>

    <label for="search_navi"> 
        <Search id="nav-search-loopsvg" />
        Search
    </label>
       
    <div id="nav-search-under"></div>
    <div id="nav-search-under-exp"></div>
</div>

<div id="nav-tree">
    <ul>

<!-- Category -->
        {#each user.active_tree as {id, name, visible, submenu}, i}{#if visible === true}                   
            <li>
                <div>{name}</div>
                <ul> <!-- Sub Category, clickable draggable-->
                    {#each submenu as {id, name, visible, draggable}, i} {#if visible === true} 
                        <li draggable={draggable}  
                            ondragstart = {(e: any) => { 
                                if ("ondragevent" in submenu[i])
                                    submenu[i].ondragevent(e)
                                /*set_drag_drop_buffer_params(submenu[i])*/ 
                            }}
                            ondragend   = {(e: any) => {
                                if ("ondropevent" in submenu[i])
                                    submenu[i].ondropevent(e)
                                //set_drag_drop_buffer_params({}) 
                            }}
                        >    
                            <button class="nav-tree-navi "  onpointerdown="{() => {
                                if (draggable) return
                                set_navigation(name, id)
                            } }" >
                                {name}
                            </button>                        
                        </li>        
                    {/if} {/each}
                </ul>
            </li>  
        {/if} {/each}
    </ul> 
        
    {#if get_debug}
        <div id="debug_msg">DEV BUILD: {get_version}</div>
    {:else}
        <div id="version">RELEASE: {get_version}</div>
    {/if}        
</div>


<style>
    #debug_msg{
        width: 85%; 
        text-align: center;
        color: #ff8a8a;
        font-size: 1.2em;
    
        position: absolute;
        bottom: 6px;
    }

    #version{
        width: 85%; 
        text-align: center;
        color: #5e6b77;
        font-size: 0.8em;
    
        position: absolute;
        bottom: 6px;
    }
</style>



