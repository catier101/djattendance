import {reset} from 'redux-form';
import initialState from './initialState'

//action types
//action creators
//WeekNav
export const NEXT_WEEK = 'NEXT_WEEK'
export const nextWeek = () => {
  return {type: NEXT_WEEK};
}

export const PREV_WEEK = 'PREV_WEEK'
export const prevWeek = () => {
  return {type: PREV_WEEK};
}

export const NEXT_PERIOD = 'NEXT_PERIOD'
export const nextPeriod = () => {
  return {type: NEXT_PERIOD};
}

export const PREV_PERIOD = 'PREV_PERIOD'
export const prevPeriod = () => {
  return {type: PREV_PERIOD};
}

//AttendanceDetails
export const TOGGLE_UNEXCUSED_ABSENCES = 'TOGGLE_UNEXCUSED_ABSENCES'
export const toggleUnexcusedAbsences = () => {
  return {type: TOGGLE_UNEXCUSED_ABSENCES};
}

export const TOGGLE_UNEXCUSED_TARDIES = 'TOGGLE_UNEXCUSED_TARDIES'
export const toggleUnexcusedTardies = () => {
  return {type: TOGGLE_UNEXCUSED_TARDIES};
}

export const TOGGLE_EXCUSED = 'TOGGLE_EXCUSED'
export const toggleExcused = () => {
  return {type: TOGGLE_EXCUSED};
}

export const TOGGLE_LEAVE_SLIPS = 'TOGGLE_LEAVE_SLIPS'
export const toggleLeaveSlips = () => {
  return {type: TOGGLE_LEAVE_SLIPS};
}

export const TOGGLE_LEAVE_SLIP_DETAIL = 'TOGGLE_LEAVE_SLIP_DETAIL'
export const toggleLeaveSlipDetail = (id, evs, slipType, TA, comments, informed) => {
  return {type: TOGGLE_LEAVE_SLIP_DETAIL, key: id, evs: evs, slipType: slipType, TA: TA, comments: comments, informed: informed};
}

//AttendanceActions
export const HIDE_ALL_FORMS =' HIDE_ALL_FORMS'
export const hideAllForms = () => {
  return {type: HIDE_ALL_FORMS};
}

export const TOGGLE_SUBMIT_ROLL = 'TOGGLE_SUBMIT_ROLL'
export const toggleSubmitRoll = () => {
  return {type: TOGGLE_SUBMIT_ROLL};
}

export const TOGGLE_SUBMIT_LEAVE_SLIP = 'TOGGLE_SUBMIT_LEAVE_SLIP'
export const toggleSubmitLeaveSlip = () => {
  return {type: TOGGLE_SUBMIT_LEAVE_SLIP};
}

export const TOGGLE_SUBMIT_GROUP_LEAVE_SLIP = 'TOGGLE_SUBMIT_GROUP_LEAVE_SLIP'
export const toggleSubmitGroupLeaveSlip = () => {
  return {type: TOGGLE_SUBMIT_GROUP_LEAVE_SLIP};
}

export const TOGGLE_OTHER_REASONS = 'TOGGLE_OTHER_REASONS'
export const toggleOtherReasons = () => {
  return {type: TOGGLE_OTHER_REASONS};
}

export const REMOVE_SELECTED_EVENT = 'REMOVE_SELECTED_EVENT'
export const removeSelectedEvent = (ev) => {
  return {type: REMOVE_SELECTED_EVENT, event: ev};
}

export const REMOVE_ALL_SELECTED_EVENTS = 'REMOVE_ALL_SELECTED_EVENTS'
export const removeAllSelectedEvents = () => {
  return {type: REMOVE_ALL_SELECTED_EVENTS};
}

//GridContainer
export const TOGGLE_EVENT = 'TOGGLE_EVENT'
export const toggleEvent = (ev) => {
  return {type: TOGGLE_EVENT, event: ev};
}

export const TOGGLE_DAYS_EVENTS = 'TOGGLE_DAYS_EVENTS' 
export const toggleDaysEvents = (evs) => {
  return {type: TOGGLE_DAYS_EVENTS, events: evs};
}

//async related, using thunks, google redux-thunk for more info

// RollSlip has fields {rollStatus, slipType, comments, informed, TAInformed}
// slipId is determine between POST (new slip, slipId == null) or PUT (update slip, slipId != null)
export const postRollSlip = (rollSlip, selectedEvents, slipId) => {
  if ((rollSlip.rollStatus !== undefined || rollSlip.rollStatus != "") 
        && (rollSlip.slipType === undefined || rollSlip.slipType == "")) {
    return function (dispatch) { 
      dispatch(postRoll(rollSlip, selectedEvents));
    }
  }
  else if ((rollSlip.rollStatus === undefined || rollSlip.rollStatus == "") 
            && (rollSlip.slipType !== undefined || rollSlip.slipType != "")) {
    return function (dispatch) { 
      dispatch(postLeaveSlip(rollSlip, selectedEvents, slipId));
    }
  }
  else if ((rollSlip.rollStatus !== undefined || rollSlip.rollStatus != "") 
            && (rollSlip.slipType !== undefined || rollSlip.slipType != "")) {
    return function (dispatch) {
      dispatch(postRoll(rollSlip, selectedEvents, slipId, true));
    }
  }
  else {
    dispatch(receiveResponse('Error no data for roll or slips'));
  }
}

export const SUBMIT_ROLL = 'SUBMIT_ROLL'
export const submitRoll = (roll) => {
  return {
    type: SUBMIT_ROLL,
    roll: roll
  }
}

export const postRoll = (rollSlip, selectedEvents, slipId = null, withSlip = false) => {
  var rolls = [];
  var roll = {
      "id": null, 
      "event": null, 
      "trainee": initialState.reducer.trainee.id, 
      "status": rollSlip.rollStatus,
      "finalized": false, 
      "notes": "", 
      "submitted_by": initialState.reducer.trainee.id, 
      "last_modified": Date.now(),
      "date": null
    }
  if (selectedEvents.length == 0) {
    //need to create an error action
    return function (dispatch) {
      dispatch(receiveResponse('error no events selected'));
    }
  }
  else {
    for (var i = 0; i < selectedEvents.length; i++) {
      rolls.push(Object.assign({}, roll, {
        event: selectedEvents[i].id,
        date: dateFns.format(selectedEvents[i].start, 'YYYY-MM-DD')
      }));
    }
  }
  return function (dispatch) {
    var data = null;
    if (rolls.length == 1) {
      data = rolls[0];
    } else {
      data = JSON.stringify(rolls);
    }

    return $.ajax({
      url: '/api/rolls/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(rolls),
      success: function (data, status, jqXHR) {
        dispatch(submitRoll(rolls));
        if (withSlip) {
          dispatch(postLeaveSlip(rollSlip, selectedEvents, slipId));
        } else {
          dispatch(receiveResponse(status));
          dispatch(reset('rollSlipForm'));
          dispatch(removeAllSelectedEvents());
          dispatch(hideAllForms());
        }
      },
      error: function (jqXHR, textStatus, errorThrown ) {
        console.log('Roll post error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}

export const SUBMIT_LEAVE_SLIP = 'SUBMIT_LEAVE_SLIP'
export const submitLeaveSlip = (slip) => {
  return {
    type: SUBMIT_LEAVE_SLIP,
    slip: slip
  }
}

export const postLeaveSlip = (rollSlip, selectedEvents, slipId) => {
  if (selectedEvents.length == 0) {
    //need to create an error action
    return function (dispatch) {
      dispatch(receiveResponse('error no events selected'));
    }
  }
  var tas = initialState.reducer.tas;
  var ta_id = null;
  for (var i = 0; i < initialState.reducer.tas.length; i++) {
    if (rollSlip.TAInformed == tas[i].firstname + ' ' + tas[i].lastname) {
      ta_id = tas[i].id
    }
  }

  var event_details = [];
  for (var i = 0; i < selectedEvents.length; i++) {
    event_details.push({"id": selectedEvents[i].id, "date": dateFns.format(selectedEvents[i].start, 'YYYY-MM-DD')});
  }
  var texted = false;
  if (rollSlip.informed == "texted") {
    texted = true;
    rollSlip.informed = false;
  }
  var slip = {
        "id": slipId, 
        "type": rollSlip.slipType,
        "status": "P", 
        "TA": ta_id, 
        "trainee": initialState.reducer.trainee.id, 
        "submitted": Date.now(), 
        "last_modified": Date.now(), 
        "finalized": null, 
        "description": "", 
        "comments": rollSlip.comments, 
        "texted": texted, 
        "informed": rollSlip.informed, 
        "events": event_details
    };

  var ajaxType = 'POST';
  var ajaxData = JSON.stringify(slip);
  if (slipId) {
    ajaxType = 'PATCH';
    ajaxData = JSON.stringify([slip]);
  }

  return function (dispatch) {
    return $.ajax({
      url: '/api/individualslips/',
      type: ajaxType,
      contentType: 'application/json',
      data: ajaxData,
      success: function (data, status, jqXHR) {
        dispatch(submitLeaveSlip(data));
        dispatch(receiveResponse(status));
        dispatch(reset('rollSlipForm'));
        dispatch(removeAllSelectedEvents());
        dispatch(hideAllForms());
      },
      error: function (jqXHR, textStatus, errorThrown ) {
        console.log('Slip post error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}

//using destroy because delete is an official HTTP action
export const DESTROY_LEAVE_SLIP = 'DESTROY_LEAVE_SLIP'
export const destroyLeaveSlip = (slipId) => {
  return {
    type: DESTROY_LEAVE_SLIP,
    slipId: slipId
  }
}

export const deleteLeaveSlip = (slipId) => {
  return function (dispatch) {
    dispatch(destroyLeaveSlip(slipId));
    return $.ajax({
      url: '/api/individualslips/' + slipId.toString(),
      type: 'DELETE',
      success: function (data, status, jqXHR) {
        dispatch(receiveResponse(status));
        dispatch(reset('rollSlipForm'));
        dispatch(removeAllSelectedEvents());
        dispatch(hideAllForms());
      },
      error: function (jqXHR, textStatus, errorThrown ) {
        console.log('Slip delete error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}


export const SUBMT_GROUP_LEAVE_SLIP = 'SUBMT_GROUP_LEAVE_SLIP'
export const submitGroupLeaveSlip = (response) => {
  return {
    type: SUBMT_GROUP_LEAVE_SLIP,
    gSlip: gSlip,
  }
}

export const postGroupLeaveSlip = (gSlip, selectedEvents) => {
  console.log(gSlip); //TODO
}

export const RECEIVE_RESPONSE = 'RECEIVE_RESPONSE'
function receiveResponse(response) {
  return {
    type: RECEIVE_RESPONSE,
    response: response,
    receivedAt: Date.now()
  }
}

