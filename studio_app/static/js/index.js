document.addEventListener("DOMContentLoaded", () => {
    $('#book_confirm_modal').on('show.bs.modal', function (event) {
      var slot_to_book = $(event.relatedTarget) // Button that triggered the modal
      var minute_modal = slot_to_book.data('minute')
      var hour_modal = slot_to_book.data('hour')
      var date_modal = slot_to_book.data('date')
      var month_modal = slot_to_book.data('month')
      var year_modal = slot_to_book.data('year')
      var modal_time_full = slot_to_book.data('full')
      // Extract info from data-* attributes
      // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var modal = $(this)
      modal.find('#minute_input').val(minute_modal)
      modal.find('#hour_input').val(hour_modal)
      modal.find('#date_input').val(date_modal)
      modal.find('#month_input').val(month_modal)
      modal.find('#year_input').val(year_modal)
      modal.find('#time_book').text(modal_time_full)


      console.log("index# $")
    })
  })