user_appointments_for_frontend.forEach(element => {
  element.at = new Date(element.at)
});
console.log(user_appointments_for_frontend)
// {
//   "at": "2024-10-30T14:00:00.000Z",
//   "done_by_id": null,
//   "lust_update_by_id": null,
//   "price": null,
//   "approved": false,
//   "description": "",
//   "deposit_needed": false,
//   "approved_by_id": null,
//   "deposit": null,
//   "approved_at": null,
//   "id": 8,
//   "slot_id": 326,
//   "canceled": false,
//   "amount_time_min": 90,
//   "canceled_at": null,
//   "user_id": 1,
//   "done": false,
//   "lust_update_at": null,
//   "service_id": 1,
//   "done_at": null,
//   "canceled_by_id": null,
//   "service_name": "manicure",
//   "service_description": "manicure",
//   "client_name": "no name",
//   "client_tel": "no telephone",
//   "client_description": "-"
// }
const options_datetime = {
  weekday: 'long',
  month: 'long',
  day: 'numeric',
  hourCycle: "h12",
  dayPeriod: "short",
  hour: "numeric",
  minute: "2-digit"
};
console.log(user_appointments_for_frontend[0].at.toLocaleString("en-US", options_datetime))

function create_card_for_appointment(appointment) {
  let card_container = document.createElement("div")
  card_container.className = "border border-white m-2 pb-1 bg-light"
  card_container.id = "appointment_" + appointment.id

  let card = document.createElement("div")
  card.className = "card mb-4 rounded-3 shadow-sm"
  card.id = card_container.id + "_card"
  card_container.appendChild(card)

  let card_header = document.createElement("div")
  card_header.className = "card-header py-1 bg-gradient"
  card_header.id = card_container.id + "_card_header"
  if (appointment.canceled) {
    card_header.className += " bg-secondary"
  } else if (appointment.done){
    card_header.className += " bg-info"
  } else if (appointment.approved) {
    card_header.className += " bg-warning"
  } else {
    card_header.className += " bg-danger"
  }
  card.appendChild(card_header)

  let card_header_content = document.createElement("div")
  card_header_content.className = "fs-5 fw-normal row"
  card_header_content.id = card_header.id + "_content"
  card_header.appendChild(card_header_content)

  let card_header_content_date = document.createElement("div")
  card_header_content_date.className = "col"
  card_header_content_date.id = card_header_content + "_date"
  card_header_content_date.textContent = appointment.at.toLocaleString("en-US", options_datetime)
  card_header_content.appendChild(card_header_content_date)

  let card_header_content_status = document.createElement("div")
  card_header_content_status.className = "col text-end"
  card_header_content_status.id = card_header_content + "_status"
  if (appointment.canceled) {
    card_header_content_status.textContent = "canceled"
  } else if (appointment.done){
    card_header_content_status.textContent = "done"
  } else if (appointment.approved) {
    card_header_content_status.textContent = "approved"
  } else {
    card_header_content_status.textContent = "pending"
  }
  card_header_content.appendChild(card_header_content_status)

  let card_body = document.createElement("div")
  card_body.className = "card-body"
  card_body.id = card_container.id + "_body"
  card_container.appendChild(card_body)

  let card_first_row_btn = document.createElement("div")
  card_first_row_btn.className ="row mx-2"
  card_container.appendChild(card_first_row_btn)

  let card_second_row_btn = document.createElement("div")
  card_second_row_btn.className ="row mx-2"
  card_container.appendChild(card_second_row_btn)

  let card_edit_btn = document.createElement("button")
  card_edit_btn.type = "button"
  card_edit_btn.className = "col m-1 w-100 btn btn-lg btn-primary py-1 mb-1"
  card_edit_btn.dataset.toggle = "modal" 
  card_edit_btn.dataset.target = "#editModal" 
  card_edit_btn.dataset.booking_id = appointment.id
  card_edit_btn.dataset.id = appointment.user_id
  card_edit_btn.dataset.datetime = appointment.at.toLocaleDateString("en-US", options_datetime) 
  card_edit_btn.dataset.service = appointment.service_name
  card_edit_btn.dataset.client = appointment.client_name + " " + appointment.client_tel  
  card_edit_btn.dataset.date_picker_format = appointment.at.toISOString().slice(0, 16)  
  card_edit_btn.dataset.duration = appointment.amount_time_min 
  card_edit_btn.dataset.message = appointment.description
  card_edit_btn.textContent = "Edit"
  card_first_row_btn.appendChild(card_edit_btn)

  let card_confirm_btn = document.createElement("button")
  card_confirm_btn.type = "button"
  card_confirm_btn.className = "col m-1 w-100 btn btn-lg btn-warning py-1 mb-1"
  card_confirm_btn.dataset.toggle = "modal" 
  card_confirm_btn.dataset.target="#confirmModal" 
  card_confirm_btn.dataset.booking_id = appointment.id
  card_confirm_btn.dataset.id = appointment.user_id
  card_confirm_btn.dataset.datetime = appointment.at.toLocaleDateString("en-US", options_datetime) 
  card_confirm_btn.dataset.service = appointment.service_name
  card_confirm_btn.dataset.client = appointment.client_name + " " + appointment.client_tel
  card_confirm_btn.dataset.message = appointment.description
  card_confirm_btn.textContent = "Confirm"
  if (appointment.approved) {
    card_confirm_btn.disabled = true
  }
  card_first_row_btn.appendChild(card_confirm_btn)

  let card_done_btn = document.createElement("button")
  card_done_btn.type = "button"
  card_done_btn.className = "col m-1 w-100 btn btn-lg btn-success py-1 mb-1"
  card_done_btn.dataset.toggle="modal" 
  card_done_btn.dataset.target="#doneModal" 
  card_done_btn.dataset.booking_id = appointment.id
  card_done_btn.dataset.id = appointment.user_id
  card_done_btn.dataset.datetime = appointment.at.toLocaleDateString("en-US", options_datetime) 
  card_done_btn.dataset.service = appointment.service_name
  card_done_btn.dataset.client = appointment.client_name + " " + appointment.client_tel
  card_done_btn.dataset.message = appointment.description
  card_done_btn.textContent = "Done"
  if (appointment.done || appointment.canceled) {
    card_done_btn.disabled = true
  }
  card_second_row_btn.appendChild(card_done_btn)

  let card_cancel_btn = document.createElement("button")
  card_cancel_btn.type = "button"
  card_cancel_btn.className = "col m-1 w-100 btn btn-lg btn-danger py-1 mb-1"
  card_cancel_btn.dataset.toggle="modal" 
  card_cancel_btn.dataset.target="#cancelModal" 
  card_cancel_btn.dataset.booking_id = appointment.id
  card_cancel_btn.dataset.id = appointment.user_id
  card_cancel_btn.dataset.datetime = appointment.at.toLocaleDateString("en-US", options_datetime) 
  card_cancel_btn.dataset.service = appointment.service_name
  card_cancel_btn.dataset.client = appointment.client_name + " " + appointment.client_tel
  card_cancel_btn.dataset.message = appointment.description
  card_cancel_btn.textContent = "Cancel"
  if (appointment.done) {
    card_cancel_btn.disabled = true
  }
  card_second_row_btn.appendChild(card_cancel_btn)

  return card_container
}

let appointment_main = document.getElementsByTagName("main")[0]
console.log(appointment_main)

for (let index = 0; index < user_appointments_for_frontend.length; index++) {
  const appointment = user_appointments_for_frontend[index];
  appointment_main.appendChild(create_card_for_appointment(appointment))
}
document.addEventListener("DOMContentLoaded", () => {
    // data-date="{{get_this_date}}" data-service="{{service}}" data-client="{{client}}"
     $('#cancelModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_cancel  = button.data('id') 
         var booking_id_cancel = button.data('booking_id')
         var date_cancel = button.data('datetime')
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
         var date_edit = button.data('datetime')
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
        //  modal.find('#new_time').val(time_edit)
         modal.find('#new_date').val(date_picker_format_edit)
         console.log(date_picker_format_edit)
         modal.find('#new_duration').val(duration_edit)
         modal.find('#new_message').val(message_edit)
         console.log(service_edit)
         if (service_edit == "manicure") {
           modal.find('#manicure').attr('checked', true)
           modal.find('#pedicure').attr('checked', false)
         } else if (service_edit == "pedicure") {

           modal.find('#pedicure').attr('checked', true)
           modal.find('#manicure').attr('checked', false)
         } else if (service_edit == "combo") {
           console.log("combo")
           modal.find('#manicure').attr('checked', true)
           modal.find('#pedicure').attr('checked', true)
         }
       })

       $('#confirmModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_confirm  = button.data('id') 
         var booking_id_confirm = button.data('booking_id')
         var date_confirm = button.data('datetime')
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
         var datetime_done = button.data('datetime')
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

