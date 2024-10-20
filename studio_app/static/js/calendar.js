!function() {

    var today = moment();
  
    function Calendar(selector, events) {
      this.el = document.querySelector(selector);
      this.events = events;
      this.current = moment().date(1);
      this.draw();
      var current = document.querySelector('.today');
      if(current) {
        var self = this;
        window.setTimeout(function() {
          self.openDay(current);
        }, 500);
      }
    }
  
    Calendar.prototype.draw = function() {
      //Create Header
      this.drawHeader();

      this.drawLegend();
  
      //Draw Month
      this.drawMonth();
  
      
    }
  
    Calendar.prototype.drawHeader = function() {
      var self = this;
      if(!this.header) {
        //Create the header elements
        this.header = createElement('div', 'header');
        this.header.className = 'header';
  
        this.title = createElement('h1');
  
        var right = createElement('div', 'right');
        right.addEventListener('click', function() { self.nextMonth(); });
  
        var left = createElement('div', 'left');
        left.addEventListener('click', function() { self.prevMonth(); });
  
        //Append the Elements
        this.header.appendChild(this.title); 
        this.header.appendChild(right);
        this.header.appendChild(left);
        this.el.appendChild(this.header);
      }
  
      this.title.innerHTML = this.current.format('MMMM YYYY');
    }
  
    Calendar.prototype.drawMonth = function() {
      var self = this;
    
      
      if(this.month) {
        this.oldMonth = this.month;
        this.oldMonth.className = 'month out ' + (self.next ? 'next' : 'prev');
        this.oldMonth.addEventListener('webkitAnimationEnd', function() {
          self.oldMonth.parentNode.removeChild(self.oldMonth);
          self.month = createElement('div', 'month');
          self.backFill();
          self.currentMonth();
          self.fowardFill();
          self.el.appendChild(self.month);
          window.setTimeout(function() {
            self.month.className = 'month in ' + (self.next ? 'next' : 'prev');
          }, 16);
        });
      } else {
          this.month = createElement('div', 'month');
          this.el.appendChild(this.month);
          this.backFill();
          this.currentMonth();
          this.fowardFill();
          this.month.className = 'month new';
      }
    }
  
    Calendar.prototype.backFill = function() {
      var clone = this.current.clone();
      var dayOfWeek = clone.day();
  
      if(!dayOfWeek) { return; }
  
      clone.subtract('days', dayOfWeek+1);
  
      for(var i = dayOfWeek; i > 0 ; i--) {
        this.drawDay(clone.add('days', 1));
      }
    }
  
    Calendar.prototype.fowardFill = function() {
      var clone = this.current.clone().add('months', 1).subtract('days', 1);
      var dayOfWeek = clone.day();
  
      if(dayOfWeek === 6) { return; }
  
      for(var i = dayOfWeek; i < 6 ; i++) {
        this.drawDay(clone.add('days', 1));
      }
    }
  
    Calendar.prototype.currentMonth = function() {
      var clone = this.current.clone();
  
      while(clone.month() === this.current.month()) {
        this.drawDay(clone);
        clone.add('days', 1);
      }
    }
  
    Calendar.prototype.getWeek = function(day) {
      if(!this.week || day.day() === 0) {
        this.week = createElement('div', 'week');
        this.month.appendChild(this.week);
      }
    }
  
    Calendar.prototype.drawDay = function(day) {
      var self = this;
      this.getWeek(day);
  
      //Outer Day
      var outer = createElement('div', this.getDayClass(day));
      outer.addEventListener('click', function() {
        self.openDay(this);
      });
  
      //Day Name
      var name = createElement('div', 'day-name', day.format('ddd'));
  
      //Day Number
      var number = createElement('div', 'day-number', day.format('DD'));
  
  
      //Events
      var events = createElement('div', 'day-events');
      if (action_path == '/book/') {
        this.drawEvents(day, events);
      }
      else if (action_path == '/windows/') {
        this.drawEvents(day, events);
       // this.drawSlots(day, events);
      }
      
  
      outer.appendChild(name);
      outer.appendChild(number);
      outer.appendChild(events);
      this.week.appendChild(outer);
    }
  
    Calendar.prototype.drawEvents = function(day, element) {
      if(day.month() === this.current.month()) {
        var todaysEvents = this.events.reduce(function(memo, ev) {
          if(ev.date.isSame(day, 'day')) {
            memo.push(ev);
          }
          return memo;
        }, []);
  
        todaysEvents.forEach(function(ev) {
          var evSpan = createElement('span', ev.color);
          element.appendChild(evSpan);
        });
      }
    }

    Calendar.prototype.drawSlots = function(day, element) {

      var days_slots = [[10, 0], [10, 30], [11, 0], [11, 30], [12, 0], [13, 0], [13, 30], [14, 0], [14, 30], [15, 0]]

      var currentWrapper = element.querySelector('.events');
      var wrapper = createElement('div', 'events in' + (currentWrapper ? ' new' : ''));

      days_slots.forEach(function(slot) {
        //var slot_time = day
        day.hour(slot[0])
        //var slot_time = 
        day.minute(slot[1])        

        var div = createElement('div', 'event');
        var square = createElement('div', 'event-category yellow');
        //var span = createElement('span', '', ev.eventName);


        var form = createElement('form');
        form.setAttribute("action", action_path);
        form.setAttribute("method", "POST");

        var input_minute = createElement('input');
        input_minute.setAttribute("type", "hidden");
        input_minute.setAttribute("name", "minute");        
        input_minute.setAttribute("value", day.minute());

        var input_hour = createElement('input');
        input_hour.setAttribute("type", "hidden");
        input_hour.setAttribute("name", "hour");
        input_hour.setAttribute("value", day.hour());

        var input_date = createElement('input');
        input_date.setAttribute("type", "hidden");
        input_date.setAttribute("name", "date");
        input_date.setAttribute("value", day.date());

        var input_month = createElement('input');
        input_month.setAttribute("type", "hidden");
        input_month.setAttribute("name", "month");
        input_month.setAttribute("value", day.month());

        var input_year = createElement('input');
        input_year.setAttribute("type", "hidden");
        input_year.setAttribute("name", "year");
        input_year.setAttribute("value", day.year()); 

        var input_slot_id = createElement('input');
        input_slot_id.setAttribute("type", "hidden");
        input_slot_id.setAttribute("name", "slot-id");
        input_slot_id.setAttribute("value", ev.id);
        
        var button = createElement('input', 'open_time');
        button.setAttribute("type", "submit");
        button.setAttribute("value", day.format('h:mm a'));
        
        form.appendChild(input_minute);
        form.appendChild(input_hour);
        form.appendChild(input_date);
        form.appendChild(input_month);
        form.appendChild(input_year);
        form.appendChild(input_slot_id)
        form.appendChild(button)

        div.appendChild(square);
        div.appendChild(form);
        wrapper.appendChild(div);
      });
      element.appendChild(wrapper)

      // if(day.month() === this.current.month()) {
      //   var todaysEvents = this.events.reduce(function(memo, ev) {
      //     if(ev.date.isSame(day, 'day')) {
      //       memo.push(ev);
      //     }
      //     return memo;
      //   }, []);
  
      //   todaysEvents.forEach(function(ev) {
      //     var evSpan = createElement('span', ev.color);
      //     element.appendChild(evSpan);
      //   });
      // }
    }
  
    Calendar.prototype.getDayClass = function(day) {
      classes = ['day'];
      if(day.month() !== this.current.month()) {
        classes.push('other');
      } else if (today.isSame(day, 'day')) {
        classes.push('today');
      }
      return classes.join(' ');
    }
  
    Calendar.prototype.openDay = function(el) {
      var details, arrow;
      var dayNumber = +el.querySelectorAll('.day-number')[0].innerText || +el.querySelectorAll('.day-number')[0].textContent;
      var day = this.current.clone().date(dayNumber);
  
      var currentOpened = document.querySelector('.details');
  
      //Check to see if there is an open detais box on the current row
      if(currentOpened && currentOpened.parentNode === el.parentNode) {
        details = currentOpened;
        arrow = document.querySelector('.arrow');
      } else {
        //Close the open events on differnt week row
        //currentOpened && currentOpened.parentNode.removeChild(currentOpened);
        if(currentOpened) {
          currentOpened.addEventListener('webkitAnimationEnd', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.addEventListener('oanimationend', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.addEventListener('msAnimationEnd', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.addEventListener('animationend', function() {
            currentOpened.parentNode.removeChild(currentOpened);
          });
          currentOpened.className = 'details out';
        }
  
        //Create the Details Container
        details = createElement('div', 'details in');
  
        //Create the arrow
        var arrow = createElement('div', 'arrow');
  
        //Create the event wrapper
  
        details.appendChild(arrow);
        el.parentNode.appendChild(details);
      }
  
      var todaysEvents = this.events.reduce(function(memo, ev) {
        if(ev.date.isSame(day, 'day')) {
          memo.push(ev);
        }
        return memo;
      }, []);
  
      this.renderEvents(todaysEvents, details);
  
      arrow.style.left = el.offsetLeft + (window.screen.width / 19) + 'px';// - el.parentNode.offsetLeft// + (window.screen.width / 5) + 'px';

    }
  
    Calendar.prototype.renderEvents = function(events, ele) {
      //Remove any events in the current details element
      var currentWrapper = ele.querySelector('.events');
      var wrapper = createElement('div', 'events in' + (currentWrapper ? ' new' : ''));
  
      events.forEach(function(ev) {
        var div = createElement('div', 'event');
        var square = createElement('div', 'event-category ' + ev.color);
        //var span = createElement('span', '', ev.eventName);
        console.log(ev)
        if (action_path == "/book/"){
                // <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" data-whatever="@mdo">Open modal for @mdo</button>
                var modal_button = createElement('button', 'btn btn-primary btn-calendar')
                modal_button.setAttribute("data-toggle", "modal")
                modal_button.setAttribute("data-target", "#book_confirm_modal")
                modal_button.setAttribute("data-slot_id", ev.id)
                modal_button.setAttribute("data-minute", ev.date.minute())
                modal_button.setAttribute("data-hour", ev.date.hour())
                modal_button.setAttribute("data-date", ev.date.date())
                modal_button.setAttribute("data-month", ev.date.month())
                modal_button.setAttribute("data-year", ev.date.year())
                modal_button.setAttribute("data-full", ev.date.format('LLLL'))
                // modal_button.setAttribute("value", ev.date.format('h:mm a'))
                modal_button.innerText = ev.date.format('llll')
                div.appendChild(modal_button);
                }
        else if (action_path == "/windows/") {
          
        var form = createElement('form');
        form.setAttribute("action", action_path);
        form.setAttribute("method", "POST");

        var input_minute = createElement('input');
        input_minute.setAttribute("type", "hidden");
        input_minute.setAttribute("name", "minute");
        input_minute.setAttribute("value", ev.date.minute());


        var input_hour = createElement('input');
        input_hour.setAttribute("type", "hidden");
        input_hour.setAttribute("name", "hour");
        input_hour.setAttribute("value", ev.date.hour());

        var input_date = createElement('input');
        input_date.setAttribute("type", "hidden");
        input_date.setAttribute("name", "date");
        input_date.setAttribute("value", ev.date.date());


        var input_month = createElement('input');
        input_month.setAttribute("type", "hidden");
        input_month.setAttribute("name", "month");
        input_month.setAttribute("value", ev.date.month());


        var input_year = createElement('input');
        input_year.setAttribute("type", "hidden");
        input_year.setAttribute("name", "year");
        input_year.setAttribute("value", ev.date.year());

        var input_slot_id = createElement('input');
        input_slot_id.setAttribute("type", "hidden");
        input_slot_id.setAttribute("name", "slot-id");
        input_slot_id.setAttribute("value", ev.id);
 
        
        var button = createElement('input', 'open_time');
        button.setAttribute("type", "submit");
        button.setAttribute("value", ev.eventName);
        
        form.appendChild(input_minute);
        form.appendChild(input_hour);
        form.appendChild(input_date);
        form.appendChild(input_month);
        form.appendChild(input_year);
        form.appendChild(input_slot_id);
        form.appendChild(button);
        div.appendChild(square);
        div.appendChild(form);
        }        
        wrapper.appendChild(div);
      });
  
      if(!events.length) {
        var div = createElement('div', 'event empty');
        var span = createElement('span', '', 'No available time for booking');
  
        div.appendChild(span);
        wrapper.appendChild(div);
      }
  
      if(currentWrapper) {
        currentWrapper.className = 'events out';
        currentWrapper.addEventListener('webkitAnimationEnd', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
        currentWrapper.addEventListener('oanimationend', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
        currentWrapper.addEventListener('msAnimationEnd', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
        currentWrapper.addEventListener('animationend', function() {
          currentWrapper.parentNode.removeChild(currentWrapper);
          ele.appendChild(wrapper);
        });
      } else {
        ele.appendChild(wrapper);
      }
    }
  
    Calendar.prototype.drawLegend = function() {
      var self = this;
      if (!this.legend) {
        this.legend = createElement('div', 'legend');
        var calendars = this.events.map(function(e) {
          return e.calendar + '|' + e.color;
        }).reduce(function(memo, e) {
          if(memo.indexOf(e) === -1) {
            memo.push(e);
          }
          return memo;
        }, []).forEach(function(e) {
          var parts = e.split('|');
          var entry = createElement('span', 'entry ' +  parts[1], parts[0]);
          self.legend.appendChild(entry);
        });
        this.el.appendChild(this.legend);
        }
 
    }
  
    Calendar.prototype.nextMonth = function() {
      this.current.add('months', 1);
      this.next = true;
      this.draw();
    }
  
    Calendar.prototype.prevMonth = function() {
      this.current.subtract('months', 1);
      this.next = false;
      this.draw();
    }
  
    window.Calendar = Calendar;
  
    function createElement(tagName, className, innerText) {
      var ele = document.createElement(tagName);
      if(className) {
        ele.className = className;
      }
      if(innerText) {
        ele.innderText = ele.textContent = innerText;
      }
      return ele;
    }
  }();
  
  !function() {
    filtered_slots = []    
    slots.forEach((slot) => {
      if (slot[1] < moment().year()) {
        
        return
      } else if (slot[1] == moment().year() && slot[2] < moment().month()+1) {        
        return
      } else if (slot[1] == moment().year() && slot[2] == moment().month()+1 && slot[3] < moment().date()) {
        return
      } else {
        filtered_slots.push(slot)
        return
      }
    })
    var data = filtered_slots.map((slot) => {
      slot_status = slot[6] == 1 ? 'Avaliable time' : 'Closed time'
      slot_color  = slot[6] == 1 ? 'green' : 'yellow'
      slot_id = slot[0]
      slot[5] = (slot[5] < 10) ? ('0' + slot[5]) : slot[5]
      var the_date = moment().minute(slot[5]).hour(slot[4]).date(slot[3]).month(slot[2] - 1).year(slot[1])
      return { eventName: the_date.format("llll"), calendar: slot_status, color: slot_color, date: the_date, id: slot_id}
    });

    // var data = [

    //   { eventName: 'Lunch Meeting w/ Mark', calendar: 'Work', color: 'orange', date: moment().date(25).month(10).year(2023) },
    //   { eventName: 'Interview - Jr. Web Developer', calendar: 'Work', color: 'orange', date: moment().date(1).month(10).year(2023) },
    //   { eventName: 'Demo New App to the Board', calendar: 'Work', color: 'orange', date: moment().date(26).month(10).year(2023) },
    //   { eventName: 'Dinner w/ Marketing', calendar: 'Work', color: 'orange', date: moment().date(15).month(10).year(2023) },
  
    //   { eventName: 'Game vs Portalnd', calendar: 'Sports', color: 'blue', date: moment().date(4).month(11).year(2023) },
    //   { eventName: 'Game vs Houston', calendar: 'Sports', color: 'blue', date: moment().date(0).month(11).year(2023) },
    //   { eventName: 'Game vs Denver', calendar: 'Sports', color: 'blue', date: moment().date(14).month(11).year(2023) },
    //   { eventName: 'Game vs San Degio', calendar: 'Sports', color: 'blue', date: moment().date(26).month(11).year(2023) },
  
    //   { eventName: '10:30', calendar: 'Kids', color: 'green', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: '10:30', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(11).year(2023) },
    //   { eventName: 'Parent/Teacher Conference', calendar: 'Kids', color: 'yellow', date: moment().date(9).month(10).year(2023) },
    //   { eventName: 'Pick up from Soccer Practice', calendar: 'Kids', color: 'yellow', date: moment().date(8).month(10).year(2023) },
    //   { eventName: 'Ice Cream Night', calendar: 'Kids', color: 'yellow', date: moment().date(6).month(8).year(2023) },
  
    //   { eventName: 'Free Tamale Night', calendar: 'Other', color: 'green', date: moment().date(0).month(0).year(2024) },
    //   { eventName: 'Bowling Team', calendar: 'Other', color: 'green', date: moment().date(11).month(0).year(2024) },
    //   { eventName: 'Teach Kids to Code', calendar: 'Other', color: 'green', date: moment().date(2).month(1).year(2024) },
    //   { eventName: 'Startup Weekend', calendar: 'Other', color: 'green', date: moment().date(22).month(1).year(2024) }
    // ];
  
    
  
    function addDate(ev) {
      
    }
  
    var calendar = new Calendar('#calendar', data);
  
  }();