document.addEventListener("DOMContentLoaded", () => {
    btn = document.getElementById("submit_code")
    input_code = document.getElementById("code")
    input_code.addEventListener("change", () => {activate_btn(btn, input_code)} )
    input_code.addEventListener("keyup", () => {activate_btn(btn, input_code)})
    function activate_btn(btn, input) {
        
        if (input.value > 999 && input.value < 10000) {
            btn.disabled = false
        } else {
            btn.disabled = true
        }
    }
})