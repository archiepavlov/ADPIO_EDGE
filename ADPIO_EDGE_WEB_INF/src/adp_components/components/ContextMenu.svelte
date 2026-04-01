<script  lang="ts">
  import ConfModal from "./ConfModal.svelte"
  
  export let buttons:any
  export let visible:boolean = false

  let props: any = {pos_x: 120, pos_y:120}

  export function open_context(x: number, y: number){
    props.pos_x = x
    props.pos_y = y
    visible = true
  }

  let modal: any = {
    visible: false,
    title: "No Title",
    description: "No Description",
    btn_accept_txt: "ACCEPT",
    btn_decline_txt: "CANCEL",
    action: () => {},
  }
</script>

<svelte:window on:click="{(e: any) => {
    visible = false
}}" />


<div class="context-menu {visible ? '' : 'context-menu-hidden'}" style="top: {props.pos_y}px; left: {props.pos_x}px;" >
  {#each buttons as btn }
    {#if !(("rendered" in btn) && !(btn.rendered)) }
      <button class="context-menu-btn {btn.disabled ? 'context-menu-btn-disabled': ''}"
        onclick={(e: any) => { 
          if (!btn.disabled){
            if (btn.with_confirmation) {
              modal = {
                visible: true,
                title: btn.conf_title,
                description: btn.conf_description,
                btn_accept_txt: btn.conf_btn_accept_txt,
                btn_decline_txt: "CANCEL",
                action: btn.onclick,
              }            
            } else {
              btn.onclick(e) 
            }
          }
        }}
      >
        <svelte:component style="scale: 1.2; padding-top: 1px; " this={btn.icon} /> 

        {btn.text} 
      </button> 
    {/if}
  {/each}
</div>

<ConfModal 
  title={modal.title} description={modal.description} 
  btn_accept_txt={modal.btn_accept_txt} btn_decline_txt={modal.btn_decline_txt}
  bind:visible={modal.visible} on_accept={(e: any) => { modal.action(e) }} 
/>  

<style>
  .context-menu {
    position: absolute;
    z-index: 999;

    display: flex;
    flex-direction: column;
    /*width: 240px;*/
    background-color: #515c66;
    justify-content: center;
    border-radius: 5px;

    opacity: 1;
    visibility: visible;

    transition: opacity 240ms linear;
  }

  .context-menu-hidden {
    opacity: 0.0;
    visibility: hidden;

    transition: opacity 240ms  linear 0ms, 
                visibility 0ms linear 240ms;
  }

  .context-menu-btn {
    background-color: transparent;
    border: none;
    padding: 4px 12px;
    color: white;
    display: flex;
    position: relative;
    gap: 16px;
    cursor: pointer;
    border-radius: 4px;
    
    transition: color 360ms linear; 
  }

  .context-menu-btn-disabled {
    color: #ffffff40 !important;
    cursor: default    !important;
  }

  .context-menu-btn:not(:active):hover,
  .context-menu-btn:focus {
    /*background-color: #21262C;*/
    color: #ff9800;
  }

  .context-menu-btn:focus,
  .context-menu-btn:active {
    /*background-color: #00ff37;*/
    outline: none;
  }

  .context-menu-btn::before {
    content: "";
    position: absolute;
    top: 5px;
    left: -10px;
    width: 5px;
    height: 80%;
    background-color: #ff9800;
    border-radius: 5px;
    opacity: 0;

    transition: opacity 180ms linear;     
  }

  .context-menu-btn:focus::before,
  .context-menu-btn:active::before {
    opacity: 1;    
  }
</style>