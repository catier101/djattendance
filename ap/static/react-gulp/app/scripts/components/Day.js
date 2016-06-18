import React, { PropTypes } from 'react'

import { joinValidClasses } from '../constants'

const Day = ({ name, num, isToday }) => (
  <div className="col-md-1 col-xs-1 no-padding days-row">
    <div className="schedule-header"
      style={{
        backgroundColor: isToday ? '#dff0d8' : '',
        borderRadius: isToday ? '2px' : ''
      }}
    >
      {name}  {num}
    </div>
  </div>
)

Day.propTypes = {
  name: PropTypes.string.isRequired,
  num: PropTypes.string.isRequired,
  isToday: PropTypes.bool.isRequired
}

export default Day