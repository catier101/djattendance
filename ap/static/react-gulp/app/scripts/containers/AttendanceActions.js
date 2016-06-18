import { connect } from 'react-redux'
import { toggleSubmitRoll, toggleSubmitLeaveSlip, toggleSubmitGroupLeaveSlip,
          toggleLeaveSlips, toggleOtherReasons, removeSelectedEvent, removeAllSelectedEvents,
          postRollSlip, postGroupLeaveSlip } from '../actions'
import ActionBar from '../components/ActionBar'

const mapStateToProps = (state) => {
  var ta_names = [];
  for (var i = 0; i < state.reducer.tas.length; i++) {
    ta_names.push(state.reducer.tas[i].firstname + ' ' + state.reducer.tas[i].lastname);
  }

  var lsdShow = false;
  for (var key in state.reducer.leaveSlipDetailsShow) {
    if (state.reducer.leaveSlipDetailsShow.hasOwnProperty(key) 
          && state.reducer.leaveSlipDetailsShow[key]) {
      lsdShow = true;
      break;
    }
  }
  return {
    submitRollShow: state.reducer.submitRollShow,
    submitLeaveSlipShow: state.reducer.submitLeaveSlipShow,
    submitGroupLeaveSlipShow: state.reducer.submitGroupLeaveSlipShow,
    otherReasonsShow: state.reducer.otherReasonsShow,
    selectedEvents: state.reducer.selectedEvents,
    submitting: state.reducer.submitting,
    formSuccess: state.reducer.formSuccess,
    trainee: state.reducer.trainee,
    isSecondYear: state.reducer.isSecondYear,
    tas: ta_names,
    lsdShow: lsdShow
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    toggleSubmitRoll: () => {
      dispatch(toggleSubmitRoll())
    },
    toggleSubmitLeaveSlip: () => {
      dispatch(toggleSubmitLeaveSlip())
    },
    toggleSubmitGroupLeaveSlip: () => {
      dispatch(toggleSubmitGroupLeaveSlip())
    },
    toggleOtherReasons: () => {
      dispatch(toggleOtherReasons())
    },
    removeSelectedEvent: (ev) => {
      dispatch(removeSelectedEvent(ev))
    },
    removeAllSelectedEvents: () => {
      dispatch(removeAllSelectedEvents())
    },
    postRollSlip: (rollSlip, selectedEvents, slipId) => { //slipId here will be null
      dispatch(postRollSlip(rollSlip, selectedEvents, slipId))
    },
    postGroupLeaveSlip: (gSlip, selectedEvents) => {
      dispatch(postGroupLeaveSlip(gSlip, selectedEvents))
    }
  }
}

const AttendanceActions = connect(
  mapStateToProps,
  mapDispatchToProps
)(ActionBar)

export default AttendanceActions