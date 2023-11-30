window.addEventListener("load", () => {
    
    const ok = document.createElement("b", "status_pic");
    ok.innerHTML = "&#10004;"
    const not_ok = document.createElement("b", "status_pic");
    not_ok.innerHTML = "&#10006;"

    const myInput = document.getElementById("password");
    const confirmation = document.getElementById("confirmation");
    const letter = document.getElementById("letter");
    const capital = document.getElementById("capital");
    const number = document.getElementById("number");
    const length = document.getElementById("length");
    const submit = document.getElementById("form_signup");
    const btn = document.getElementById("signup_submit");

    letter.prepend(document.createElement("b", "status_pic"));
    letter.status_pic.innerHTML = "&#10006;"
    capital.prepend(not_ok);
    number.prepend(not_ok);
    length.prepend(not_ok);
    // pass_same.prepend(not_ok);

    var is_letter = false;
    var is_capital = false;
    var is_number = false;
    var is_length = false;
    var is_same = false;


    // When the user clicks on the password field, show the message box
    // myInput.onfocus = function() {
    // document.getElementById("message").style.display = "block";
    // }

    // When the user clicks outside of the password field, hide the message box
    // myInput.onblur = function() {
    // document.getElementById("message").style.display = "none";
    // }

    //validate password and confirmation are not the same

    function set_valid_invalid (element, is_valid, to_disable) {
        if (is_valid == true) {
            to_disable.forEach(el => {
                el.disabled = false;
            })
            element.classList.remove("invalid");
            element.classList.add("valid");
            element.status_pic.remove();
            element.prepend(ok);
        } else {
            to_disable.forEach(el => {
                el.disabled = true;
            })
            element.classList.remove("valid");
            element.classList.add("invalid");
            element.status_pic.remove();
            element.prepend(not_ok);

        }
        

    }
    submit.addEventListener("submit", (event) => {
        if (myInput.value != confirmation.value) {
            event.preventDefault();
        };
    })

    // When the user starts to type something inside the password field
    myInput.onkeyup = function() {

    // Validate the same
    if(myInput.value != confirmation.value) {

    } else {

    }

    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    is_letter = myInput.value.match(lowerCaseLetters);
    if(is_letter) {
        set_valid_invalid(letter, is_letter, [btn]);
        letter_before.innerHTML = ok;
        
    } else {
        set_valid_invalid(letter, false, [btn]);
        letter_before.innerHTML = not_ok;
        
    }

    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if(myInput.value.match(upperCaseLetters)) {
        btn.disabled = false;
        capital.classList.remove("invalid");
        capital.classList.add("valid");
        capital_before.innerHTML = ok;
        is_capital = true;
    } else {
        capital.classList.remove("valid");
        btn.disabled = true;
        capital.classList.add("invalid");
        capital_before.innerHTML = not_ok;
    }

    // Validate numbers
    var numbers = /[0-9]/g;
    if(myInput.value.match(numbers)) {
        btn.disabled = false;
        number.classList.remove("invalid");
        number.classList.add("valid");
        number_before.innerHTML = ok;
        is_number = true;
    } else {
        btn.disabled = true;
        number.classList.remove("valid");
        number.classList.add("invalid");
        number_before.innerHTML = not_ok;
    }

    // Validate length
    if(myInput.value.length >= 8) {
        btn.disabled = false;
        length.classList.remove("invalid");
        length.classList.add("valid");
        length_before.innerHTML = ok;
        is_length = true;
    } else {
        btn.disabled = true;
        length.classList.remove("valid");
        length.classList.add("invalid");
        length_before.innerHTML = not_ok;
    }
    }
})

