<script  lang="ts">
    import { onDestroy }      from 'svelte'

    import { 
        async_post,
    } from "../../stores"

    import Modal from "./Modal.svelte";

    export let log_file: string = 'system'
    export let header  : string = 'SYSTEM'

    let terminal_modal : any
    let content        : any = []
    let update_interval: number = -1

    export async function open(e: any){
        terminal_modal.open(e.clientX - 560, e.clientY + 35)

        await start_interval()
        await update()
    }

    async function update(){
        let res = await async_post( '/logger', 'show_logs', { file: log_file } )
        content = res.content
        //console.log(content)
    }

    async function start_interval(){
        if (update_interval > -1) return
        update_interval = setInterval(async () => { 
            await update()
        }, 3000)      
    }


    onDestroy(async () => { 
        clearInterval(update_interval) 
        update_interval = -1
    })  
</script>


    <Modal bind:this={terminal_modal} title="TERMINAL: {header}" onclose={(e: any) => { 
        clearInterval(update_interval)  
        update_interval = -1
    }} >
        <div class="terminal-body">
            <div>
                {#each content as ln }
                    <div>{ln}</div>    
                {/each}
            </div>  
        </div>
    </Modal>

<style>

.terminal-body {
    background-color: #333333;
    color: #ffffff;
    padding: 12px;

    height: 420px;
    width:  680px;

    overflow-y: auto; 
    overflow-x: auto; 
    display: flex;
    flex-direction: column;

    font-size: 0.85em;
    flex-direction: column-reverse;
}

.terminal-body > div  {
    width: 1536px;
    
}

.terminal-body > div > div {
    display: flex;
    align-items: center;
    white-space: break-spaces;
    min-height: 20px;
}

    
</style>