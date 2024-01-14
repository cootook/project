
    
    const ok = document.createElement("b");
    ok.classList.add("status_pic");
    ok.innerHTML = "&#10004;"
    const not_ok = document.createElement("b");
    not_ok.classList.add("status_pic");
    not_ok.innerHTML = "&#10006;"

    const myInput = document.getElementById("password");
    const confirmation = document.getElementById("confirmation");
    const letter = document.getElementById("letter");
    const capital = document.getElementById("capital");
    const number = document.getElementById("number");
    const length = document.getElementById("length");
    const pass_same = document.getElementById("pass_same");
    const submit = document.getElementById("form_signup");
    const btn = document.getElementById("signup_submit");

    letter.prepend(not_ok.cloneNode(true));
    capital.prepend(not_ok.cloneNode(true));
    number.prepend(not_ok.cloneNode(true));
    length.prepend(not_ok.cloneNode(true));
    pass_same.prepend(not_ok.cloneNode(true));

    var is_letter = false;
    var is_capital = false;
    var is_number = false;
    var is_length = false;
    var is_same = false;
    var is_recaptcha = false;

    function set_is_recaptcha_false() {
        is_recaptcha = false;
        validate_pass()
        console.log("recaptcha false")    
    }
    
    function set_is_recaptcha_true() {
        is_recaptcha = true;
        validate_pass()
        console.log("recaptcha true")
    }

    //validate password and confirmation are not the same

    function set_valid_invalid (element, is_valid, to_disable) {
        if (is_valid) {
            element.classList.remove("invalid");
            element.classList.add("valid");
            element.querySelector(".status_pic").remove();
            element.prepend(ok.cloneNode(true));
        } else {
            element.classList.remove("valid");
            element.classList.add("invalid");
            element.querySelector(".status_pic").remove();
            element.prepend(not_ok.cloneNode(true));

        }

        to_disable.forEach(el => {
            if(
                is_letter &&
                is_capital &&
                is_number &&
                is_length &&
                is_same &&
                is_recaptcha) {
                    el.disabled = false;
                } else {
                    el.disabled = true;
                }
            
        })
        

    }
    
    function validate_pass() {

        // Validate the same
        is_same = myInput.value == confirmation.value;
        console.log(is_same)
        console.log(myInput.value)
        console.log(confirmation.value)
        set_valid_invalid(pass_same, is_same, [btn]);
    
        // Validate lowercase letters
        var lowerCaseLetters = /[a-z]/g;
        is_letter = myInput.value.match(lowerCaseLetters);
        set_valid_invalid(letter, is_letter, [btn]);
    
        // Validate capital letters
        var upperCaseLetters = /[A-Z]/g;
        is_capital = myInput.value.match(upperCaseLetters);
        set_valid_invalid(capital, is_capital, [btn]);  
    
        // Validate numbers
        var numbers = /[0-9]/g;
        is_number = myInput.value.match(numbers);
        set_valid_invalid(number, is_number, [btn]);
     
        // Validate length
        is_length = myInput.value.length >= 6;
        set_valid_invalid(length, is_length, [btn])
        }

    submit.addEventListener("submit", (event) => {
        if (!is_letter ||
            !is_capital ||
            !is_number ||
            !is_length ||
            !is_same) {
            event.preventDefault();
        };
    })

    // When the user starts to type something inside the password field
    myInput.onkeyup = validate_pass;
    confirmation.onkeyup = validate_pass;


