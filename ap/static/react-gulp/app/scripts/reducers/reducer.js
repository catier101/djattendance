import { NEXT_WEEK, PREV_WEEK, NEXT_PERIOD, PREV_PERIOD, 
         TOGGLE_UNEXCUSED_ABSENCES, TOGGLE_UNEXCUSED_TARDIES, TOGGLE_EXCUSED, TOGGLE_LEAVE_SLIPS, TOGGLE_LEAVE_SLIP_DETAIL,
         HIDE_ALL_FORMS, TOGGLE_SUBMIT_ROLL, TOGGLE_SUBMIT_LEAVE_SLIP, TOGGLE_SUBMIT_GROUP_LEAVE_SLIP, TOGGLE_OTHER_REASONS,
         REMOVE_SELECTED_EVENT, REMOVE_ALL_SELECTED_EVENTS, TOGGLE_EVENT, TOGGLE_DAYS_EVENTS, 
         SUBMIT_ROLL, SUBMIT_LEAVE_SLIP, DESTROY_LEAVE_SLIP, SUBMIT_GROUP_LEAVE_SLIP, RECEIVE_RESPONSE } from '../actions';
import { LEAVE_SLIP_OTHER_TYPES, sortEvents } from '../constants'
import initialState from '../initialState';

function reducer(state = initialState, action) {
  switch (action.type) {
    //WeekNav
    case PREV_WEEK:
      return Object.assign({}, state, {
        date: dateFns.addDays(state.date, -7)
      });
    case NEXT_WEEK:
      return Object.assign({}, state, {
        date: dateFns.addDays(state.date, 7)
      });
    case PREV_PERIOD:
      return Object.assign({}, state, {
        date: dateFns.addDays(state.date, -14)
      });
    case NEXT_PERIOD:
      return Object.assign({}, state, {
        date: dateFns.addDays(state.date, 14)
      });
    //AttendanceDetail
    case TOGGLE_UNEXCUSED_ABSENCES:
      return Object.assign({}, state, {
        unexcusedAbsencesShow: !state.unexcusedAbsencesShow
      });
    case TOGGLE_UNEXCUSED_TARDIES:
      return Object.assign({}, state, {
        unexcusedTardiesShow: !state.unexcusedTardiesShow
      });
    case TOGGLE_EXCUSED:
      return Object.assign({}, state, {
        excusedShow: !state.excusedShow
      });
    case TOGGLE_LEAVE_SLIPS:
      return Object.assign({}, state, {
        leaveSlipsShow: !state.leaveSlipsShow
      });
    case TOGGLE_LEAVE_SLIP_DETAIL:
      if (state.leaveSlipDetailsShow[action.key]) {
        state.leaveSlipDetailsShow[action.key] = false;
        var newLeaveSlipDetailsShow = Object.assign({}, state.leaveSlipDetailsShow)
        return Object.assign({}, state, {
          leaveSlipDetailsShow: newLeaveSlipDetailsShow,
          leaveSlipDetailFormValues: {
            slipType: "",
            comments: "",
            informed: "true",
            TAInformed: ""
          },
          selectedEvents: [],
          otherReasonsShow: false
        })
      }

      for (var key in state.leaveSlipDetailsShow) {
        if (key == action.key) {
          state.leaveSlipDetailsShow[action.key] = !state.leaveSlipDetailsShow[action.key];
        } else {
          state.leaveSlipDetailsShow[key] = false;
        }
      }
      var newLeaveSlipDetailsShow = Object.assign({}, state.leaveSlipDetailsShow)

      var taName = "";
      for (var i = 0; i < state.tas.length; i++) {
        if (state.tas[i].id == action.TA) {
          taName = state.tas[i].firstname + " " + state.tas[i].lastname;
          break;
        }
      }

      state.leaveSlipDetailFormValues = {
        slipType: action.slipType,
        comments: action.comments,
        informed: action.informed.toString(),
        TAInformed: taName
      }
      var newInitialFormValues = Object.assign({}, state.leaveSlipDetailFormValues);

      var slipEvents = [];
      if (newLeaveSlipDetailsShow[action.key]) {
        for (var i = 0; i < action.evs.length; i++) {
          for (var j = 0; j < state.events.length; j++) {
            if (action.evs[i].id == state.events[j].id
                  && action.evs[i].date == dateFns.format(state.events[j].start, 'YYYY-MM-DD')) {
              slipEvents.push(state.events[j]);
            }
          }
        }
      }

      var showOtherReasons = false;
      if (LEAVE_SLIP_OTHER_TYPES.indexOf(action.slipType) != -1 ) {
        showOtherReasons = true;
      }

      return Object.assign({}, state, {
          leaveSlipDetailsShow: newLeaveSlipDetailsShow,
          leaveSlipDetailFormValues: newInitialFormValues,
          selectedEvents: slipEvents.sort(sortEvents),
          submitRollShow: false,
          submitLeaveSlipShow: false,
          otherReasonsShow: showOtherReasons
        })
    //AttendanceActions
    case HIDE_ALL_FORMS:
      return Object.assign({}, state, {
        submitRollShow: false,
        submitLeaveSlipShow: false,
        submitGroupLeaveSlipShow: false,
      }); 
    case TOGGLE_SUBMIT_ROLL:
      return Object.assign({}, state, {
        submitRollShow: !state.submitRollShow,
        submitGroupLeaveSlipShow: false,
      });
    case TOGGLE_SUBMIT_LEAVE_SLIP:
      var anyLeaveSlipDetailsShowing = false;

      for (var key in state.leaveSlipDetailsShow) {
        if (state.leaveSlipDetailsShow[key]) {
          anyLeaveSlipDetailsShowing = true;
          state.leaveSlipDetailsShow[key] = false;
        }
      }

      if (anyLeaveSlipDetailsShowing) {
        var newLeaveSlipDetailsShow = Object.assign({}, state.leaveSlipDetailsShow)

        return Object.assign({}, state, {
          selectedEvents: [],
          submitLeaveSlipShow: !state.submitLeaveSlipShow,
          submitGroupLeaveSlipShow: false,
          otherReasonsShow: false,
          leaveSlipDetailsShow: newLeaveSlipDetailsShow,
          leaveSlipDetailFormValues: {
              slipType: "",
              comments: "",
              informed: "true",
              TAInformed: ""
            },
        });
      } else {
        return Object.assign({}, state, {
          submitLeaveSlipShow: !state.submitLeaveSlipShow,
          submitGroupLeaveSlipShow: false,
        });
      }
        
    case TOGGLE_SUBMIT_GROUP_LEAVE_SLIP:
      return Object.assign({}, state, {
        submitRollShow: false,
        submitLeaveSlipShow: false,
        submitGroupLeaveSlipShow: !state.submitGroupLeaveSlipShow
      });
    case TOGGLE_OTHER_REASONS:
      return Object.assign({}, state, {
        otherReasonsShow: !state.otherReasonsShow
      });
    case REMOVE_SELECTED_EVENT:
      for (var i = 0; i < state.selectedEvents.length; i++) {
        if (action.event == state.selectedEvents[i]) {
          state.selectedEvents.splice(i, 1);
        }
      }

      if (state.selectedEvents.length == 0) {
        return Object.assign({}, state, {
          submitRollShow: false,
          submitLeaveSlipShow: false,
          selectedEvents: []
        });
      }
      return Object.assign({}, state, {
        selectedEvents: state.selectedEvents.slice()
      });
    case REMOVE_ALL_SELECTED_EVENTS:
      return Object.assign({}, state, {
        submitRollShow: false,
        submitLeaveSlipShow: false,
        selectedEvents: []
      });
    //GridContainer
    case TOGGLE_EVENT:
      var nSE = null;
      for (var i = 0; i < state.selectedEvents.length; i++) {
        if (action.event == state.selectedEvents[i]) {
          state.selectedEvents.splice(i, 1);
          nSE = state.selectedEvents.slice();
          return Object.assign({}, state, {
            submitRollShow: nSE.length == 0 ? false : true && state.isSecondYear,
            submitLeaveSlipShow: nSE.length == 0 ? false : true,
            selectedEvents: nSE
          });
        }
      }
      nSE = state.selectedEvents.slice();
      nSE.push(action.event);
      nSE.sort(sortEvents)
      return Object.assign({}, state, {
        submitRollShow: nSE.length == 0 ? false : true && state.isSecondYear,
        submitLeaveSlipShow: nSE.length == 0 ? false : true,
        selectedEvents: nSE
      });
    case TOGGLE_DAYS_EVENTS:
      var evs = action.events.slice();
      for (var i = 0; i < state.selectedEvents.length; i++) {
        for (var j = 0; j < action.events.length; j++) {
          if (action.events[j] == state.selectedEvents[i]) {
            action.events.splice(j, 1);
          }
        }
      }
      if (action.events.length != 0) {
        return Object.assign({}, state, {
          selectedEvents: state.selectedEvents.concat(action.events).slice()
        });
      }
      for (var i = 0; i < state.selectedEvents.length; i++) {
        for (var j = 0; j < evs.length; j++) {
          if (evs[j] == state.selectedEvents[i]) {
            state.selectedEvents.splice(i, 1);
          }
        }
      }
      return Object.assign({}, state, {
        selectedEvents: state.selectedEvents.slice()
      });
    //Async related
    case SUBMIT_ROLL:
      if (action.roll.length == 1) {
        for (var i = 0; i < state.eventsSlipsRolls.length; i++) {
          if (state.eventsSlipsRolls[i].event.id == action.roll[0].event
              && dateFns.format(state.eventsSlipsRolls[i].event.start, "YYYY-MM-DD") == action.roll[0].date) {
            state.eventsSlipsRolls[i].roll = action.roll[0];
          }
        }

        var nEsr = state.eventsSlipsRolls.slice();

        return Object.assign({}, state, {
          submitting: true,
          eventsSlipsRolls: nEsr,
          rolls: [
            ...state.rolls,
            action.roll[0]
          ]
        });
      } else {
        for (var i = 0; i < state.eventsSlipsRolls.length; i++) {
          for (var j = 0; j < action.roll.length; j++) {
            if (state.eventsSlipsRolls[i].event.id == action.roll[j].event
                && dateFns.format(state.eventsSlipsRolls[i].event.start, "YYYY-MM-DD") == action.roll[j].date) {
              state.eventsSlipsRolls[i].roll = action.roll[j];
            }
          }
        }
        var nEsr = state.eventsSlipsRolls.slice();
        var nRolls = state.rolls.concat(action.roll);
        return Object.assign({}, state, {
          submitting: true,
          eventsSlipsRolls: nEsr,
          rolls: nRolls
        });
      }
    case SUBMIT_LEAVE_SLIP:
      if (action.slip.constructor === Array) {
        action.slip = action.slip[0]
      }
      for (var i = 0; i < state.eventsSlipsRolls.length; i++) {
        for (var j = 0; j < action.slip.events.length; j++) {
          if (state.eventsSlipsRolls[i].event.id == action.slip.events[j].id
                && dateFns.format(state.eventsSlipsRolls[i].event.start, 'YYYY-MM-DD') == action.slip.events[j].date) {
            state.eventsSlipsRolls[i].slip = action.slip;
            break;
          }
        }
      }

      state.leaveSlipDetailsShow[action.slip.id] = false;

      var nEsr = state.eventsSlipsRolls.slice();
      return Object.assign({}, state, {
        submitting: true,
        eventsSlipsRolls: nEsr,
        slips: [
          ...state.slips,
          action.slip
        ],
        leaveSlipDetailsShow: Object.assign({}, state.leaveSlipDetailsShow)
      });
    case DESTROY_LEAVE_SLIP:
      for (var i = 0; i < state.eventsSlipsRolls.length; i++) {
        if (state.eventsSlipsRolls[i].slip && (state.eventsSlipsRolls[i].slip.id == action.slipId)) {
          state.eventsSlipsRolls[i].slip = null;
        }
      }
      var newEsrs = state.eventsSlipsRolls.slice(); 

      var newSlips = null;
      for (var i = 0; i < state.slips.length; i++) {
        if (state.slips[i].id == action.slipId) {
          newSlips = state.slips.splice(i, 1);
        }
      }

      delete state.leaveSlipDetailsShow[action.slipId];
      var newLeaveSlipDetailsShow = Object.assign({}, state.leaveSlipDetailsShow);

      return Object.assign({}, state, {
        slips: newSlips,
        eventsSlipsRolls: newEsrs,
        leaveSlipDetailsShow: newLeaveSlipDetailsShow
      });
    case SUBMIT_GROUP_LEAVE_SLIP:
      return state //TODO
    case RECEIVE_RESPONSE:
      return Object.assign({}, state, {
        submitting: false
      });
    default:
      return state;
  }
}

export default reducer