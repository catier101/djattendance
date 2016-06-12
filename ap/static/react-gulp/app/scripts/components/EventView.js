import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { Button, OverlayTrigger, Popover } from 'react-bootstrap'

import { ATTENDANCE_STATUS_LOOKUP, SLIP_STATUS_LOOKUP, EVENT_CODE_LOOKUP, FA_ICON_LOOKUP, joinValidClasses } from '../constants'

const EventView = ({ event, roll, slip, onClick, selectedEvents }) => {
  var slipStatus = slip ? slip['status'] : '';
  var rollStatus = roll ? ATTENDANCE_STATUS_LOOKUP[roll['status']] : '';
  
  var slipClasses = joinValidClasses(['slip', SLIP_STATUS_LOOKUP[slipStatus]]);
  var rollClasses = joinValidClasses([rollStatus, todayClass, 'schedule-event', 'col-md-1', 'col-xs-1']);

  if (rollStatus == 'left-class') {
    rollStatus = 'left class';
  }

  var selected = false;
  for (var i = 0; i < selectedEvents.length; i++) {
    if (event.id == selectedEvents[i].id) {
      selected = true;
    }
  }

  var todayClass = (event.id === 'TODAY') ? 'today-marker' : '';

  var h = dateFns.differenceInMinutes(event['end'], event['start'])/3*2
  h = h > 11 ? h : 12

  var divStyle = {
    top: dateFns.differenceInMinutes(dateFns.subHours(event['start'], 6), dateFns.startOfDay(event['start']))/3*2,
    height: h,
    opacity: selected ? 0.5 : 1,
  };

  var rollPopover = rollStatus ? 'Roll: ' + rollStatus : '';
  var slipPopover = slipStatus ? 'Slip: ' + SLIP_STATUS_LOOKUP[slipStatus] : '';
  var faClasses = "fa fa-" + FA_ICON_LOOKUP[SLIP_STATUS_LOOKUP[slipStatus]];


  if (roll && slip) {
    return (
      <OverlayTrigger placement="bottom" overlay={<Popover style={{display: "inline-block"}}>{rollPopover}<br></br> {slipPopover}</Popover>}>
        <div className={rollClasses} style={divStyle} onClick={onClick}>
            {EVENT_CODE_LOOKUP[event['code']]}
          <div className={slipClasses}><i className={faClasses} aria-hidden="true"></i></div>
        </div>
      </OverlayTrigger>
    )
  }

  if (!roll && slip) {
    return (
      <OverlayTrigger placement="bottom" overlay={<Popover style={{display: "inline-block"}}>{slipPopover}</Popover>}>
        <div className={rollClasses} style={divStyle} onClick={onClick}>
            {EVENT_CODE_LOOKUP[event['code']]}
          <div className={slipClasses}><i className={faClasses} aria-hidden="true"></i></div>
        </div>
      </OverlayTrigger>
    )
  }

  return (
    <div className={rollClasses} style={divStyle} onClick={onClick}>
        {EVENT_CODE_LOOKUP[event['code']]}
      <div className={slipClasses}><i className={faClasses} aria-hidden="true"></i></div>
    </div>
  )
}

EventView.propTypes = {
  event: PropTypes.object.isRequired,
  roll: PropTypes.object.isRequired,
  slip: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}

export default EventView
