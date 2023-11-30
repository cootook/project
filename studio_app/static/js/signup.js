window.addEventListener("load", () => {
    const myInput = document.getElementById("password");
    const confirmation = document.getElementById("confirmation");
    const letter = document.getElementById("letter");
    const capital = document.getElementById("capital");
    const number = document.getElementById("number");
    const length = document.getElementById("length");
    const submit = document.getElementById("signup_submit")

    const letter_before = document.getElementById("letter_before");
    const capital_before = document.getElementById("capital_before");
    const number_before = document.getElementById("number_before");
    const length_before = document.getElementById("length_before");

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

    //prevent submit if password and confirmation are not the same
    
    submit.addEventListener("submit", () => {
        if (true) {
            return;
        }
    })

    // When the user starts to type something inside the password field
    myInput.onkeyup = function() {

    // Validate lowercase letters
    var lowerCaseLetters = /[a-z]/g;
    if(myInput.value.match(lowerCaseLetters)) {
        letter.classList.remove("invalid");
        letter.classList.add("valid");
        letter_before.innerHTML = "&#10004;";
        
    } else {
        letter.classList.remove("valid");
        letter.classList.add("invalid");
        letter_before.innerHTML = "&#10006;";
        
    }

    // Validate capital letters
    var upperCaseLetters = /[A-Z]/g;
    if(myInput.value.match(upperCaseLetters)) {
        capital.classList.remove("invalid");
        capital.classList.add("valid");
        capital_before.innerHTML = "&#10004;";
    } else {
        capital.classList.remove("valid");
        capital.classList.add("invalid");
        capital_before.innerHTML = "&#10006;";
    }

    // Validate numbers
    var numbers = /[0-9]/g;
    if(myInput.value.match(numbers)) {
        number.classList.remove("invalid");
        number.classList.add("valid");
        number_before.innerHTML = "&#10004;";
    } else {
        number.classList.remove("valid");
        number.classList.add("invalid");
        number_before.innerHTML = "&#10006;";
    }

    // Validate length
    if(myInput.value.length >= 8) {
        length.classList.remove("invalid");
        length.classList.add("valid");
        length_before.innerHTML = "&#10004;";
    } else {
        length.classList.remove("valid");
        length.classList.add("invalid");
        length_before.innerHTML = "&#10006;";
    }
    }
})

