var actions = require("../actions");
var trainee = require("../testdata/trainee");
var events = require("../testdata/events");
var rolls = require("../testdata/rolls")
var slips = require("../testdata/leaveSlips")

var attendanceStore = Reflux.createStore({
  listenables: [actions],

  getInitialState: function() {
    this.state = {
      events: events,
      trainee: trainee,
      date: moment(),
      selectedEvents: {},
      selectedReason: '',
      weekEvents: [],
      rolls: rolls,
      slips: slips,
      showLeaveSlip: false
    };
    return this.state;
  },
  initEvents: function() {
    //Events should include last roll data into it
    //request.get('api/events/?trainee=[id]').end(function(){
    //  this.state.events = res;
    //});
  },
  handleDate: function(input) {
    var delta = (input === 'prev') ? -7 : 7;
    this.state.date.add('d', delta);
    this.trigger(this.state);
  },
  onNextWeek: function() {
    this.handleDate('next');
  },
  onPrevWeek: function() {
    this.handleDate('prev');
  },
  toggleEvent: function(ev) {
    // Add remove selected events based on toggle
    if (!(ev.id in this.state.selectedEvents)) {
      this.state.selectedEvents[ev.id] = ev;
    } else {
      delete this.state.selectedEvents[ev.id];
    }
    this.trigger(this.state);
  },
  //removes selected state of any reasons, removes selcted reasons, and closes the leave slip pane
  disableLeaveSlip: function() {
    this.state.showLeaveSlip = false;
    if (this.state.selectedReason!='') {
      document.getElementById(this.state.selectedReason).setAttribute('class','btn btn-info btn-primary custom')
      this.state.selectedReason = '';
      document.getElementById('comment').value='';
    }
    this.trigger(this.state);
  },
  //toggles the leave slip pane
  toggleLeaveSlip: function() {
    this.state.showLeaveSlip = !this.state.showLeaveSlip
    this.trigger(this.state);
  },
  //currently only edits existing test data.
  setRollStatus: function(status) {
    if (_.size(this.state.selectedEvents) <= 0) {
      alert('Please select at 1 event before updating the status');
      return false;
    }
    var rolls = this.state.rolls;
    var keys = [];
    //gets the ids of the selected events.
    for(var k in this.state.selectedEvents) {
      keys.push(k);
    }
    var i = 0;
    var j = 0;
    //iterates to match roll events and selectedEvents events and sets status
    while (i < rolls.length) {
      while (j < keys.length) {
        if (rolls[i].event == this.state.selectedEvents[keys[j]].id) {
          this.state.rolls[i].status = status;
          break;
        }
        j++;
      }
      j=0;
      i++;
    }
    this.trigger(this.state);
    alert('Roll Submitted');
  },
  //sets the current selected reason for a leave slip and activates/deactivates reasons accordingly.
  setLeaveSlipReason: function(reason) {
    if (this.state.selectedReason=='') {
      this.state.selectedReason=reason;
      document.getElementById(this.state.selectedReason).setAttribute('class','btn btn-info btn-primary custom active')
    } else if (this.state.selectedReason==reason) {
      document.getElementById(this.state.selectedReason).setAttribute('class','btn btn-info btn-primary custom')
      this.state.selectedReason='';
    } else {
      document.getElementById(this.state.selectedReason).setAttribute('class','btn btn-info btn-primary custom')
      this.state.selectedReason=reason;
      document.getElementById(this.state.selectedReason).setAttribute('class','btn btn-info btn-primary custom active')
    }
    this.trigger(this.state)
  },
  //currently edits leave slips with reason and comments
  submitLeaveSlip: function(text) {
    if (_.size(this.state.selectedReason) <= 0) {
      alert('Please select a reason before submitting your leave slip');
      return false;
    } else {
      var text = document.getElementById('comment').value;
      var slips = this.state.slips;
      var keys = [];
      for(var k in this.state.selectedEvents) {keys.push(k);}
      var i = 0;
      var j = 0;
      //iterates to match a selected event key with a leave slip event, then sets all the events in that leave slip to the given reason
      //not really working
      //sets comment for the leave slip
      for (i = 0; i < keys.length; i++) {
        for (j=0; j < slips.length; j++) {
          for (k=0; k < slips[j].events.length; k++) {
            if (slips[j].events[k] == this.state.selectedEvents[keys[i]].id) {
              for (var l in this.state.slips[j].events) {
                this.state.slips[l].type = this.state.selectedReason;
                this.state.slips[l].comments = text;
              }
              break;
            }
          }
        }
      }

      document.getElementById('comment').value='';
      document.getElementById(this.state.selectedReason).setAttribute('class','btn btn-info btn-primary custom')
      this.state.showLeaveSlip = false;
      this.trigger(this.state);
      alert('Leave Slip Submitted');
      }
    }
})

module.exports = attendanceStore;