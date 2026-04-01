<script  lang="ts">
    import { 
      random_id
    } from "../../stores"

export let label      :string=""
export let value      :any
export let readonly   :boolean = false

export let text_false :string = ""
export let text_true  :string  = ""

export let onchange = function(e: any){}

const r_id:string = random_id()

</script>

<div class="flex">
  {#if label !== ""}
    <div class="toggle-text">{label}</div>
  {/if}

  <div class="toggle-switch">
    <input class="toggle-input" id="toggle_{r_id}" type="checkbox" checked={value} onclick={(e:any) => {  
      if (readonly) return 
        value = !value 
        onchange(e)
    } } >


    <label class="toggle-label" for="toggle_{r_id}"></label>
  </div>

  {#if (text_true !== "") && (text_false !== "")}
    <div class="togle-text">
      {#if value}
          {text_true} 
      {:else}
          {text_false}
      {/if}
    </div>  
  {/if}


  {#if value === '≠'}
      <span>≠</span>
  {/if}
    
</div>


<style>
  .toggle-text {
    font-size: smaller;
    color: #9b9b9b;

    padding-top: 2px;
    padding-right: 8px;
  }
  
  .toggle-switch {
    position: relative;
    display: inline-block;
    width: 40px;
    height: 24px;
    /*margin: 10px;*/
  }

  .toggle-switch .toggle-input {
    display: none;
  }

  .toggle-switch .toggle-label {
    position: absolute;
    top: 0;
    left: 0;
    width: 40px;
    height: 24px;
    background-color: #969696;
    border-radius: 34px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .toggle-switch .toggle-label::before {
    content: "";
    position: absolute;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    top: 2px;
    left: 2px;
    background-color: #fff;
    box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s;
  }

  .toggle-switch .toggle-input:checked + .toggle-label {
    background-color: #4CAF50;
  }
  .toggle-switch .toggle-input:checked + .toggle-label::before {
    transform: translateX(16px);
  }

  .togle-text{
    padding-left: 6px;
  }

  /* Light Theme 
  .toggle-switch.light .toggle-label {
    background-color: #BEBEBE;
  }

  .toggle-switch.light .toggle-input:checked + .toggle-label {
    background-color: #9B9B9B;
  }

  .toggle-switch.light .toggle-input:checked + .toggle-label::before {
    transform: translateX(6px);
  }*/

  /* Dark Theme 
  .toggle-switch.dark .toggle-label {
    background-color: #4B4B4B;
  }
  .toggle-switch.dark .toggle-input:checked + .toggle-label {
    background-color: #717171;
  }
  .toggle-switch.dark .toggle-input:checked + .toggle-label::before {
    transform: translateX(16px);
  }*/

</style>