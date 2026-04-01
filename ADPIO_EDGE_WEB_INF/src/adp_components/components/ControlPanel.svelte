<script  lang="ts">
    import ButtonR    from "./ButtonR.svelte"

    export let buttons:any
</script>

    {#each buttons as btn }
        <ButtonR 
            icon                = {btn.icon}   
            text                = {btn.text}
            color               = {btn.color} 
                
            disabled            = {('disabled' in btn)?  btn.disabled : false}
            rendered            = {('rendered' in btn)?  btn.rendered : true}

            onclick             = {(e: any) => { btn.onclick(e) }}      
                
            with_confirmation   = {btn.with_confirmation}
            conf_title          = {btn.conf_title}
            conf_description    = {btn.conf_description}
            conf_btn_accept_txt = {btn.conf_btn_accept_txt}                
        />
    {/each}


<style>

</style>

