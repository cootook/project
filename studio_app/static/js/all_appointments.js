user_appointments_for_frontend.forEach(element => {
  element.at = new Date(element.at)
});

const options_datetime = {
  weekday: 'long',
  month: 'long',
  day: 'numeric',
  hourCycle: "h12",
  dayPeriod: "short",
  hour: "numeric",
  minute: "2-digit"
};

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

  let card_info = document.createElement("div")
  card_info.className = "card_info bg-dark p-2 m-1"
  card_info.id = card_container.id + "_info"

  let info_service = document.createElement("div")
  let info_service_text = document.createElement("p")
  info_service_text.textContent = "Service: " + appointment.service
  info_service.appendChild(info_service_text)
  card_info.appendChild(info_service)

  let info_description = document.createElement("div")
  let info_description_text = document.createElement("p")
  info_description_text.textContent = "Message: " + appointment.description
  info_description.appendChild(info_description_text)
  card_info.appendChild(info_description)
 
  let info_name = document.createElement("div")
  let info_name_text = document.createElement("p")
  info_name_text.textContent = "Client name: " + appointment.client_name
  info_name.appendChild(info_name_text)
  card_info.appendChild(info_name)
 
  let info_telephone = document.createElement("div")
  let info_telephone_text = document.createElement("p")
  info_telephone_text.textContent = "Phone: " + appointment.client_tel
  info_telephone.appendChild(info_telephone_text)
  card_info.appendChild(info_telephone)

  let info_about_client = document.createElement("div")
  let info_about_client_text = document.createElement("p")
  info_about_client_text.textContent = "About client: " + appointment.client_description
  info_about_client.appendChild(info_about_client_text)
  card_info.appendChild(info_about_client)

  card_body.appendChild(card_info)


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
  card_edit_btn.dataset.service = appointment.service
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
  card_confirm_btn.dataset.service = appointment.service
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
  card_done_btn.dataset.service = appointment.service
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
  card_cancel_btn.dataset.service = appointment.service
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
         var modal = $(this)            
         modal.find('#user_id_edit').val(user_id_edit)
         modal.find('#booking_id_edit').val(booking_id_edit)
         modal.find('#date_edit').text(date_edit)
         modal.find('#service_edit').text(service_edit)
         modal.find('#client_edit').text(name_edit)
         modal.find('#new_date').val(date_picker_format_edit)
         modal.find('#new_duration').val(duration_edit)
         modal.find('#new_message').val(message_edit)

         const service_as_arr = service_edit.split(",")
         checkboxes = document.getElementsByClassName("form-check-input")
         for (const element of checkboxes) {
          element.checked = false
         }
         service_as_arr.forEach(service_in_arr => {
          let checkbox_for_service = document.getElementById(service_in_arr)
          if (checkbox_for_service != null) {
            checkbox_for_service.checked = true
          }
         });
       })

       $('#confirmModal').on('show.bs.modal', function (event) {
         var button = $(event.relatedTarget) // Button that triggered the modal
         var user_id_confirm  = button.data('id') 
         var booking_id_confirm = button.data('booking_id')
         var date_confirm = button.data('datetime')
         var service_confirm = button.data('service')
         var name_confirm = button.data('client')
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
         var modal = $(this)            
         modal.find('#user_id_done').val(user_id_done)
         modal.find('#booking_id_done').val(booking_id_done)
         modal.find('#date_done').text(date_done)
         modal.find('#service_done').text(service_done)
         modal.find('#client_done').text(name_done)
       })
 })
