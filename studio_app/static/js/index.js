let recaptcha_checked = false;
document.addEventListener("DOMContentLoaded", () => {
    $('#book_confirm_modal').on('show.bs.modal', function (event) {
      var slot_to_book = $(event.relatedTarget) // Button that triggered the modal
      var slot_id_modal = slot_to_book.data('slot_id')
      console.log(slot_id_modal)
      var minute_modal = slot_to_book.data('minute')
      var hour_modal = slot_to_book.data('hour')
      var date_modal = slot_to_book.data('date')
      var month_modal = slot_to_book.data('month')
      var year_modal = slot_to_book.data('year')
      var modal_time_full = slot_to_book.data('full')
      var modal = $(this)
      modal.find('#slot_id_input').val(slot_id_modal)
      modal.find('#minute_input').val(minute_modal)
      modal.find('#hour_input').val(hour_modal)
      modal.find('#date_input').val(date_modal)
      modal.find('#month_input').val(month_modal)
      modal.find('#year_input').val(year_modal)
      modal.find('#time_book').text(modal_time_full)

      service_checkboxes = document.getElementsByClassName("service-check")
       for (const check of service_checkboxes) {
        check.addEventListener('change', submit_btn_active)
       }
      
    })
  })

  function submit_btn_active() {
    service_check_collection = document.getElementsByClassName("service-check")
    let btn = document.getElementById('submit_booking_btn');
    let at_least_one_checked = false
    for (const check of service_check_collection) {
      if (check.checked) {
        console.log(check.checked)
        at_least_one_checked = true
      }
    }

    if (recaptcha_checked && at_least_one_checked) {
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