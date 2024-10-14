const login = document.getElementById("login");
const pass = document.getElementById("password");
const signin_form = document.getElementById("signin-form");
const btn = document.getElementById("signin-submit");

let pass_not_empty = false;
let login_not_empty = false;
let is_recaptcha_valid = false;

function set_is_recaptcha_false() {
    is_recaptcha_valid = false;
    enable_btn(pass_not_empty, login_not_empty, is_recaptcha_valid, btn);
}

function set_is_recaptcha_true() {
    login_not_empty = check_input_not_empty(login);
    pass_not_empty = check_input_not_empty(pass);
    is_recaptcha_valid = true;
    enable_btn(pass_not_empty, login_not_empty, is_recaptcha_valid, btn);
}

function check_input_not_empty(input) {

    if (input.value == 0 ) {

        return false;
    }

    return true;
}

function enable_btn(is_pass, is_login, is_recaptcha, target_btn) {


    if (is_pass & is_login & is_recaptcha) {
        target_btn.disabled = false;
    } 
    else {
        target_btn.disabled = true;
    }
}

login.addEventListener("input", () => {

    login_not_empty = check_input_not_empty(login);
    pass_not_empty = check_input_not_empty(pass);
    enable_btn(pass_not_empty, login_not_empty, is_recaptcha_valid, btn);
}
);

pass.addEventListener("input", () => {
    login_not_empty = check_input_not_empty(login);
    pass_not_empty = check_input_not_empty(pass);
    enable_btn(pass_not_empty, login_not_empty, is_recaptcha_valid, btn);
}
);

document.addEventListener("any", () => {
    login_not_empty = check_input_not_empty(login);
    pass_not_empty = check_input_not_empty(pass);
    enable_btn(pass_not_empty, login_not_empty, is_recaptcha_valid, btn);
    console.log("DOMContentLoaded")
    })