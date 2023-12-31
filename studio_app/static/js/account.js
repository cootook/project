(() => {
    let convert_id_to_elements = (id_arr) => {
        res = []
        id_arr.forEach(el => {
            res.push(document.getElementById(el))
        })
        return res
    }

    let enable_editing = (inputs_arr, to_show_arr, to_hide_arr) => {
        inputs_arr.forEach(el => {
            el.disabled = false
        })
        to_hide_arr.forEach(el => {
            el.hidden = true
        })
        to_show_arr.forEach(el => {
            el.hidden = false
        })
    }

    let disable_editing = (inputs_arr, to_show_arr, to_hide_arr) => {
        inputs_arr.forEach(el => {
            el.disabled = true
        })
        to_hide_arr.forEach(el => {
            el.hodden = false
        })
        to_show_arr.forEach(el => {
            el.hidden = true
        })
    }



    let id_inputs_to_enable = [
    'notification', 
    'subscribtion', 
    'tel', 
    'client_name', 
    'username', 
    'subscribtion',
    'notification'
    ]

    let id_el_to_hide = ['edit_btn']

    let id_el_to_show = ['savet_btn']

    let inputs_to_enable = convert_id_to_elements(id_inputs_to_enable)
    let el_to_hide = convert_id_to_elements(id_el_to_hide)
    let el_to_show = convert_id_to_elements(id_el_to_show)

    document.getElementById('edit_btn').addEventListener('click', ev => {
        ev.preventDefault()
        enable_editing(inputs_to_enable, el_to_show, el_to_hide)
    })

    // document.getElementById('savet_btn').addEventListener('submit', ev => {
    //     disable_editing(inputs_to_enable, el_to_show, el_to_hide)
    // })


})()