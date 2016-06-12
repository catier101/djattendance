import { connect } from 'react-redux'
import { toggleUnexcusedAbsences, toggleUnexcusedTardies, toggleExcused, 
          toggleLeaveSlips, toggleLeaveSlipDetail, toggleOtherReasons,
          postRollSlip, deleteLeaveSlip, removeSelectedEvent, removeAllSelectedEvents } from '../actions'
import { sortEsr, sortSlips } from '../constants'
import DetailsBar from '../components/DetailsBar'

const mapStateToProps = (state) => {
  var weekStart = dateFns.format(dateFns.startOfWeek(state.reducer.date, {weekStartsAt: 1}), 'M/D/YY'),
      weekEnd = dateFns.format(dateFns.endOfWeek(state.reducer.date, {weekStartsAt: 1}), 'M/D/YY');

  //get just this week's events
  var wesr = _.filter(state.reducer.eventsSlipsRolls, function(esr) {
    return (new Date(weekStart) < new Date(esr.event['start']) && new Date(weekEnd) > new Date(esr.event['end']));
  }, this);
  
  var unexcusedAbsences = [];
  for (var i = 0; i < wesr.length; i++) {
    if ((wesr[i].slip === null || wesr[i].slip["status"] == "D" || wesr[i].slip["status"] == "P" || wesr[i].slip["status"] == "F")
           && (wesr[i].roll && wesr[i].roll["status"] == "A")) {
      unexcusedAbsences.push(wesr[i]);
    }
  }
  unexcusedAbsences = unexcusedAbsences.sort(sortEsr);

  var unexcusedTardies = [];
  for (var i = 0; i < wesr.length; i++) {
    if ((wesr[i].slip === null || wesr[i].slip["status"] == "D" || wesr[i].slip["status"] == "P" || wesr[i].slip["status"] == "F")
           && (wesr[i].roll && (wesr[i].roll["status"] == "T" || wesr[i].roll["status"] == "U" || wesr[i].roll["status"] == "L"))) {
      unexcusedTardies.push(wesr[i]);
    }
  }
  unexcusedTardies = unexcusedTardies.sort(sortEsr);

  var excused = [];
  for (var i = 0; i < wesr.length; i++) {
    if (wesr[i].slip && wesr[i].slip["status"] == "A") {
      excused.push(wesr[i]);
    }
  }
  excused = excused.sort(sortEsr);

  var slips = { 
    pending: [],
    denied: [],
    approved: []
  }
  for (var i = 0; i < wesr.length; i++) {
    if (wesr[i].slip !== null) {
      if ((wesr[i].slip["status"] == "A" || wesr[i].slip["status"] == "S") && _.indexOf(slips.approved, wesr[i].slip) == -1) {
        slips.approved.push(wesr[i].slip);
      }
      else if (wesr[i].slip["status"] == "D" && _.indexOf(slips.denied, wesr[i].slip) == -1) {
        slips.denied.push(wesr[i].slip);
      }
      else if ((wesr[i].slip["status"] == "P" || wesr[i].slip["status"] == "F") && _.indexOf(slips.pending, wesr[i].slip) == -1) {
        slips.pending.push(wesr[i].slip);
      }
    }
  }
  slips.pending = slips.pending.sort(sortSlips);
  slips.denied = slips.denied.sort(sortSlips);
  slips.approved = slips.approved.sort(sortSlips);

  var ta_names = [];
  for (var i = 0; i < state.reducer.tas.length; i++) {
    ta_names.push(state.reducer.tas[i].firstname + ' ' + state.reducer.tas[i].lastname);
  }
  return {
    unexcusedAbsences: unexcusedAbsences,
    unexcusedTardies: unexcusedTardies,
    excused: excused,
    slips: slips,
    unexcusedAbsencesShow: state.reducer.unexcusedAbsencesShow,
    unexcusedTardiesShow: state.reducer.unexcusedTardiesShow,
    excusedShow: state.reducer.excusedShow,
    leaveSlipsShow: state.reducer.leaveSlipsShow,
    leaveSlipDetailsShow: state.reducer.leaveSlipDetailsShow,
    otherReasonsShow: state.reducer.otherReasonsShow,
    selectedEvents: state.reducer.selectedEvents,
    tas: ta_names,
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    postRollSlip: (rollSlip, selectedEvents, slipId) => {
      dispatch(postRollSlip(rollSlip, selectedEvents, slipId))
    },
    deleteSlip: (slipId) => {
      dispatch(deleteLeaveSlip(slipId))
    },
    onAbsencesToggle: () => {
      dispatch(toggleUnexcusedAbsences())
    },
    onTardiesToggle: () => {
      dispatch(toggleUnexcusedTardies())
    },
    onExcusedToggle: () => {
      dispatch(toggleExcused())
    },
    toggleLeaveSlips: () => {
      dispatch(toggleLeaveSlips())
    },
    toggleLeaveSlipDetail: (id, evs, slipType, TA, comments, informed) => {
      dispatch(toggleLeaveSlipDetail(id, evs, slipType, TA, comments, informed))
    },
    toggleOtherReasons: () => {
      dispatch(toggleOtherReasons())
    },
    removeAllSelectedEvents: () => {
      dispatch(removeAllSelectedEvents())
    },
    removeSelectedEvent: (ev) => {
      dispatch(removeSelectedEvent(ev))
    }
  }
}

const AttendanceDetails = connect(
  mapStateToProps,
  mapDispatchToProps
)(DetailsBar)

export default AttendanceDetails