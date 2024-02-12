document.addEventListener("DOMContentLoaded", () => {
    // data-date="{{get_this_date}}" data-service="{{service}}" data-client="{{client}}"
     $('#cancelModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_cancel  = button.data('id') 
         var booking_id_cancel = button.data('booking_id')
         var date_cancel = button.data('date')
         var service_cancel = button.data('service')
         var name_cancel = button.data('client')
         var cancel_message = button.data('message')
         console.log(user_id_cancel, booking_id_cancel, date_cancel, service_cancel, name_cancel)// Extract info from data-* attributes
         // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
         // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
         var modal = $(this)            
         modal.find('#user_id_cancel').val(user_id_cancel)
         modal.find('#booking_id_cancel').val(booking_id_cancel)
         modal.find('#cancel_message').val(cancel_message)
         modal.find('#date_cancel').text(date_cancel)
         modal.find('#service_cancel').text(service_cancel)
         modal.find('#client_cancel').text(name_cancel)
       })

       $('#editModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_edit = button.data('id') 
         var booking_id_edit = button.data('booking_id')
         var date_edit = button.data('date')
         var service_edit = button.data('service')
         var name_edit = button.data('client')
         var time_edit = button.data('time')
         var date_picker_format_edit = button.data('date_picker_format')
         var duration_edit = button.data('duration')
         var message_edit = button.data('message')
         
         // Extract info from data-* attributes
         // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
         // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
         var modal = $(this)            
         modal.find('#user_id_edit').val(user_id_edit)
         modal.find('#booking_id_edit').val(booking_id_edit)
         modal.find('#date_edit').text(date_edit)
         modal.find('#service_edit').text(service_edit)
         modal.find('#client_edit').text(name_edit)
         modal.find('#new_time').val(time_edit)
         modal.find('#new_date').val(date_picker_format_edit)
         console.log(date_picker_format_edit)
         modal.find('#new_duration').val(duration_edit)
         modal.find('#new_message').val(message_edit)
         console.log(service_edit)
         if (service_edit == "manicure") {
           modal.find('#new_manicure').attr('checked', true)
           modal.find('#new_pedicure').attr('checked', false)
         } else if (service_edit == "pedicure") {

           modal.find('#new_pedicure').attr('checked', true)
           modal.find('#new_manicure').attr('checked', false)
         } else if (service_edit == "combo") {
           console.log("combo")
           modal.find('#new_manicure').attr('checked', true)
           modal.find('#new_pedicure').attr('checked', true)
         }
       })

       $('#confirmModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_confirm  = button.data('id') 
         var booking_id_confirm = button.data('booking_id')
         var date_confirm = button.data('date')
         var service_confirm = button.data('service')
         var name_confirm = button.data('client')
         console.log(user_id_confirm, booking_id_confirm, date_confirm, service_confirm, name_confirm)// Extract info from data-* attributes
         // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
         // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
         var modal = $(this)            
         modal.find('#user_id_confirm').val(user_id_confirm)
         modal.find('#booking_id_confirm').val(booking_id_confirm)
         modal.find('#date_confirm').text(date_confirm)
         modal.find('#service_confirm').text(service_confirm)
         modal.find('#client_confirm').text(name_confirm)
       })

       $('#doneModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_done  = button.data('id') 
         var booking_id_done = button.data('booking_id')
         var date_done = button.data('date')
         var service_done = button.data('service')
         var name_done = button.data('client')
         console.log(user_id_done, booking_id_done, date_done, service_done, name_done)// Extract info from data-* attributes
         // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
         // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
         var modal = $(this)            
         modal.find('#user_id_done').val(user_id_done)
         modal.find('#booking_id_done').val(booking_id_done)
         modal.find('#date_done').text(date_done)
         modal.find('#service_done').text(service_done)
         modal.find('#client_done').text(name_done)
       })
 })