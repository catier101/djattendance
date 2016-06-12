var trainee = require("./testdata/trainee");
var tas = require("./testdata/tas")
var events = require("./testdata/events");
var rolls = require("./testdata/rolls");
var slips = require("./testdata/slips");

//see attendance_react.html
if (typeof Trainee !== 'undefined') {
  if (Trainee.constructor === Array) {
    trainee = Trainee[0];
  } else {
    trainee = Trainee;
  } 
}
if (typeof TAs !== 'undefined') {
  tas = TAs;
}
if (typeof Events !== 'undefined') {
  events = Events;
}
if (typeof Rolls !== 'undefined') {
  rolls = Rolls;
}
if (typeof Slips !== 'undefined') {
  slips = Slips;
}

var isSecondYear = true
if (trainee.terms_attended[trainee.terms_attended.length-1] <= 2) {
  var isSecondYear = false;
}

//combine events and slips
var events_slips = [];
for (var i = 0; i < events.length; i++) {
  var ev = events[i];
  var event_slip = { event : ev,
                     slip  : null }
  for (var j = 0; j < slips.length; j++) {
    var sl = slips[j];
    for (var k = 0; k < sl.events.length; k++) {
      if (ev.id == sl.events[k].id && dateFns.format(ev.start, 'YYYY-MM-DD') == sl.events[k].date) {
        event_slip.slip = sl;
        break;
      }
    }

    if (event_slip.slip) {
      break;
    }
  }

  events_slips.push(event_slip);
}

//combine events and slips and rolls
var events_slips_rolls = [];
for (var i = 0; i < events_slips.length; i++) {
  var ev = events_slips[i].event;
  var sl = events_slips[i].slip;
  var event_slip_roll = { event : ev,
                          slip  : sl,
                          roll  : null }
  for (var j = 0; j < rolls.length; j++) {
    if (ev.id == rolls[j].event && dateFns.format(ev.start, 'YYYY-MM-DD') == rolls[j].date) {
      event_slip_roll.roll = rolls[j];
      break;
    }
  }

  events_slips_rolls.push(event_slip_roll);
}

//collapse status of each LeaveSlipDetail
var leaveSlipDetailsShow = {};
for (var i = 0; i < slips.length; i++) {
  leaveSlipDetailsShow[slips[i].id] = false;
}

var initialState = {
    form: {
      rollSlipForm: {}
    },
    reducer: {
      trainee: trainee,
      isSecondYear: isSecondYear, 
      tas: tas,
      events: events,
      rolls: rolls,
      slips: slips,
      eventsSlipsRolls: events_slips_rolls,
      date: new Date(),
      selectedEvents: [],
      leaveSlipDetailsShow: leaveSlipDetailsShow,
      leaveSlipDetailFormValues: {
            slipType: "",
            comments: "",
            informed: "true",
            TAInformed: ""
          },
      unexcusedAbsencesShow: true,
      unexcusedTardiesShow: true,
      excusedShow: true,
      submitRollShow: false,
      submitLeaveSlipShow: false,
      submitGroupLeaveSlipShow: false,
      leaveSlipsShow: false,
      otherReasonsShow: false,
      submitting: false,
      formSuccess: null,
    }
  };

module.exports = initialState;