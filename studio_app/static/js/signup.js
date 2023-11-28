window.addEventListener("load", () => {
    var myInput = document.getElementById("password");
    var letter = document.getElementById("letter");
    var capital = document.getElementById("capital");
    var number = document.getElementById("number");
    var length = document.getElementById("length");

    var letter_before = document.getElementById("letter_before");
    var capital_before = document.getElementById("capital_before");
    var number_before = document.getElementById("number_before");
    var length_before = document.getElementById("length_before");

    // When the user clicks on the password field, show the message box
    // myInput.onfocus = function() {
    // document.getElementById("message").style.display = "block";
    // }

    // When the user clicks outside of the password field, hide the message box
    // myInput.onblur = function() {
    // document.getElementById("message").style.display = "none";
    // }

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

