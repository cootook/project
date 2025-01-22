let recaptcha_checked = false;

document.addEventListener("DOMContentLoaded", () => {
    $('#book_confirm_modal').on('show.bs.modal', function (event) {
      var slot_to_book = $(event.relatedTarget) // Button that triggered the modal

      var slot_id_modal = slot_to_book.data('slot_id')
      var date_local = slot_to_book.data('date-local')
      var hour_iso_8601 = slot_to_book.data('datetime-iso')
      var modal = $(this)
      modal.find('#slot_id_input').val(slot_id_modal)
      modal.find('#datetime-iso').val(hour_iso_8601)
      modal.find('#date-local').text(date_local)
      service_checkboxes = document.getElementsByClassName("service-check")
       for (const check of service_checkboxes) {
        check.addEventListener('change', submit_btn_active)
       }
      
    })

    const input = document.querySelector("#phone");
    const phone_valid = document.querySelector("#phone_valid")
    const phone_not_valid = document.querySelector("#phone_not_valid")

    const terms_and_privacy_checkbox = document.getElementById("terms_and_privacy")
    terms_and_privacy_checkbox.addEventListener('change', submit_btn_active)


    const iti = window.intlTelInput(input, {
      initialCountry: "us",
      containerClass: "w-100",
      hiddenInput: () => ({ phone: "full_phone", country: "country_code" }),
      loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@25.1.1/build/js/utils.js"),
    });

    const validate = () => {
        if (iti.isValidNumber()) {
          phone_not_valid.hidden = true
          phone_valid.hidden = false
        } else {
          phone_not_valid.hidden = false
          phone_valid.hidden = true
        }
        submit_btn_active()
     }

     input.addEventListener("change", validate)
     input.addEventListener("keyup", validate)


  })

  function submit_btn_active() {
    service_check_collection = document.getElementsByClassName("service-check")
    let btn = document.getElementById('submit_booking_btn');
    const terms_and_privacy = document.getElementById("terms_and_privacy")
    const is_phone_invalid = document.querySelector("#phone_valid").hidden
    let at_least_one_checked = false
    for (const check of service_check_collection) {
      if (check.checked) {
        at_least_one_checked = true
      }
    }
    console.log(terms_and_privacy.checked)
    if (recaptcha_checked && at_least_one_checked && !is_phone_invalid && terms_and_privacy.checked) {
      btn.disabled = false;
    } else {
      btn.disabled = true;
    }
  }

  function enable_submit_book() {
    recaptcha_checked = true;
    submit_btn_active();
    return
  }

  function disable_submit_book() {
    btn.disabled = true;
    submit_btn_active();    
    return
  }

