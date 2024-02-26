# Databsse schema

Here is a description of db_v2.db

![schema](./images/db_schema.png)

[diagram online editor](https://dbdiagram.io/d/project-65da6aad5cd0412774bb423c)

```
Table users {
  id integer [primary key] 
  email string[320] [not null, unique]
  password string
  active bool [not null]
  fs_uniquifier string [not null, unique, note: "64 bytes"] 
  confirmed_at datetime
  last_login_at datetime
  current_login_at datetime
  last_login_ip string
  current_login_ip string
  login_count integer
  mf_recovery_codes list
  name string [not null]
  lang string [not null]
  instagram string [not null]
  tel string [not null]
  internal_note string
  subscribed_promo bool [not null]
  instagram_notification bool [not null]
  email_notification bool [not null]
  text_notification bool [not null]
  avatar_path string
}

Table role {
  id integer [primary key]
  name string [not null, unique]
  description string
}

Table user_role {
  id integer [primary key]
  user_id integer [not null, ref: <> users.id]
  role_id integer [not null, ref: <> role.id]
  set_by integer [not null, ref: <> users.id]
  set_at datetime [not null]
}

Table slots {
  id integer [primary key] 
  date_time datetime [not null]
  open bool [not null]
  opened_by integer [not null, ref: <> users.id]
  opened_at datetime [not null]
  occupied bool [not null]
  occupied_by_appoint integer [ref: <> appointments.id]
}

Table appointments {
  id integer [primary key]
  user_id integer [not null, ref: <> users.id]
  service_id integer [not null, ref: <> services.id]
  at datetime [not null]
  price float 
  deposit_needed bool [not null]
  deposit float
  slot_id integer [ref: <> slots.id]
  amount_time_min integer [not null]
  done bool [not null]
  done_by integer [ref: <> users.id] 
  done_at datetime 
  approved bool [not null]
  approved_by integer [ref: <> users.id]
  approved_at datetime 
  canceled bool [not null]
  canceled_by integer [ref: <> users.id]
  canceled_at datetime
  lust_update_at datetime
  lust_update_by integer [ref: <> users.id]
  description string
}

Table booking_messages {
  id integer [primary key]
  appoint_id integer [not null, ref: <> appointments.id]
  author_id integer [not null, ref: <> users.id]
  at datetime [not null]
  edited_at datetime
  deleted bool [not null]
}

Table services {
  id integer [primary key]
  name string [not null, unique]
  description string
}

Table service_role {
  id integer [primary key]
  service_id integer [not null, ref: <> services.id]
  role_id integer [not null, ref: <> role.id]
}

Table payments {
  id integer [primary key]
  method_id integer [not null, ref: <> payment_methods.id]
  type_id integer [not null, ref: <> payment_types.id]
  amount float [not null]
  payed bool [not null]
  status_id integer [ref: <> payment_statuses.id]
  accepted_by integer [not null, ref: <> users.id]
  payed_by integer [not null, ref: <> users.id]
  at datetime [not null]
  lust_update_at datetime
  lust_update_by integer [ref: <> users.id]
  description string
}

Table payment_methods {
  id integer [primary key]
  name string [not null, unique]
  description string
}

Table payment_statuses {
  id integer [primary key]
  name string [not null, unique]
  description string
}

Table payment_types {
  id integer [primary key]
  name string [not null, unique]
  description string
}
```