const email = document.getElementById("email");
const pass = document.getElementById("password");
const btn = document.getElementById("signin-submit");

let pass_not_empty = false;
let email_not_empty = false;
let is_recaptcha_valid = false;

function set_is_recaptcha_false() {
    is_recaptcha_valid = false;
    enable_btn(pass_not_empty, email_not_empty, is_recaptcha_valid, btn);

    console.log("set_is_recaptcha_false", pass_not_empty, email_not_empty, is_recaptcha_valid)
}

function set_is_recaptcha_true() {
    email_not_empty = check_input_not_empty(email);
    pass_not_empty = check_input_not_empty(pass);
    is_recaptcha_valid = true;
    enable_btn(pass_not_empty, email_not_empty, is_recaptcha_valid, btn);

    console.log("set_is_recaptcha_true", pass_not_empty, email_not_empty, is_recaptcha_valid)
}

function check_input_not_empty(input) {
    console.log("check_input_not_empty")

    if (input.value == 0 ) {
        console.log("check_input_not_empty -- empty")

        return false;
    }
    console.log("check_input_not_empty -- filled")
    return true;
}

function enable_btn(is_pass, is_email, is_recaptcha, target_btn) {
    console.log("enable_btn")

    if (is_pass & is_email & is_recaptcha) {
        console.log("enable_btn", is_pass, is_email, is_recaptcha)
        target_btn.disabled = false;
    } 
    else {
        console.log("enable_btn -- else", is_pass, is_email, is_recaptcha)
        target_btn.disabled = true;
    }
}

email.addEventListener("input", () => {
    console.log('email.addEventListener("input"')
    email_not_empty = check_input_not_empty(email);
    pass_not_empty = check_input_not_empty(pass);
    enable_btn(pass_not_empty, email_not_empty, is_recaptcha_valid, btn);
}
);

pass.addEventListener("input", () => {
    console.log('pass.addEventListener("input"')
    email_not_empty = check_input_not_empty(email);
    pass_not_empty = check_input_not_empty(pass);
    enable_btn(pass_not_empty, email_not_empty, is_recaptcha_valid, btn);
}
);

document.addEventListener("any", () => {
    console.log('document.addEventListener("any"')
    email_not_empty = check_input_not_empty(email);
    pass_not_empty = check_input_not_empty(pass);
    enable_btn(pass_not_empty, email_not_empty, is_recaptcha_valid, btn);
    })