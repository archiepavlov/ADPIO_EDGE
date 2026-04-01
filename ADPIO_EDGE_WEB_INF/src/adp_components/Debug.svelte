<script  lang="ts">
    import InputSelector from "./components/InputSelector.svelte"
    import InputLabel    from "./components/InputLabel.svelte"
    import InputNumber   from "./components/InputNumber.svelte"
    import InputPassword from "./components/InputPassword.svelte"
    import InputSwitch   from "./components/InputSwitch.svelte"
    import InputDropList from "./components/InputDropList.svelte"
    import SignalPanel   from "./components/SignalPanel.svelte"

    let test_value_str: string = 'Test Val str'
    let test_bool: boolean = true

    let test_float: number = 22.4
    let test_int:   number = 11

    let dropdown: any = "Value2"
    let drop_down_list:any = [
        {name: "Item 1", value: "Item 1", row_style: ""},
        {name: "Item 2", value: "Item 2", row_style: ""},
        {name: "Item 3", value: "Item 3", row_style: ""},
        {name: "Item 4", value: "Item 4", row_style: ""},
    ]

</script>


<div class="test-div content-panel">
    Signal Panel:

    <SignalPanel />
</div>

<div class="test-div content-panel"><InputLabel     label="test lablel"   bind:value={test_value_str} /></div>
<div class="test-div content-panel"><InputNumber    label="Test Float"    bind:value={test_float} type="float" step={0.5}/></div>
<div class="test-div content-panel"><InputNumber    label="Test Integr"   bind:value={test_int}   type="int" /></div>
<div class="test-div content-panel"><InputPassword  label="test password" bind:value={test_value_str} /></div>
<div class="test-div content-panel"><InputSwitch    label="test swithc"   bind:value={test_bool}  /> 
    <span style="padding-left: 50px;">Test Val = {test_bool}</span>
</div>
<div class="test-div content-panel">
    <InputSelector bind:value={dropdown} item_list={drop_down_list} label="Test Lable"    />
    <span style="padding-left: 50px;">Test Val = {dropdown}</span>
</div>

<div class="test-div content-panel">
    <InputDropList bind:value={dropdown} item_list={drop_down_list} label="Test Lable"    />
    <span style="padding-left: 50px;">Test Val = {dropdown}</span>
</div>

<style>
    .test-div {
        padding: 25px;
    }
</style>