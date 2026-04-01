<script  lang="ts">
    export let text :string = "....|...."
    export let show :boolean
    export let x    :string
    export let y    :string
</script>

<span class="tooltip {show? 'tooltip_hover' : ''}" style="transform: translate({x}, {y});">{text}</span>

<style>
    .tooltip {
        --background-tooltip: #6e7681; 
        background: var(--background-tooltip);

        position: absolute;
        z-index: 999;

        padding: 0.6em;
        opacity: 0;
        pointer-events: none;
        
        
        color: white; 
        border-radius: 8px;

        font-size: smaller;
        text-align: center;

        transition-property: all;
        transition-duration: 0.3s;
        transition-delay:    1.0s;    
    }    

    .tooltip_hover {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
    }

</style>