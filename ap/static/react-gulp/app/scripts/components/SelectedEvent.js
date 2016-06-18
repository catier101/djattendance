import React, { PropTypes } from 'react'
import { Well } from 'react-bootstrap'

import { EVENT_CODE_LOOKUP } from '../constants'

const SelectedEvent = ({ name, code, start, onClick, selectedEvents }) => {
  var count = 0;
  var duplicate = false;
  if (selectedEvents) {
    for (var i = 0; i < selectedEvents.length; i++) {
      if (code == selectedEvents[i].code) {
        count += 1;
        if (count == 2) {
          duplicate = true;
          break;
        }
      }
    }
  }

  if (duplicate) {
    return (
      <span className="selected-event">
        <span style={{paddingRight: "3px", cursor: "pointer"}} onClick={onClick}>x</span>
        {EVENT_CODE_LOOKUP[code]} {dateFns.format(start, 'M/D')}
      </span>
    )    
  }

  return (
    <span className="selected-event">
      <span style={{paddingRight: "3px", cursor: "pointer"}} onClick={onClick}>x</span>
      {EVENT_CODE_LOOKUP[code]}
    </span>
  )
}

SelectedEvent.propTypes = {
  name: PropTypes.string.isRequired,
  code: PropTypes.string.isRequired,
  start: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

export default SelectedEvent