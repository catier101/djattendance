import React, { PropTypes } from 'react'
import Day from './Day'

const DaysRow = ({days}) => (
  <div>
    <div className="col-md-1 col-xs-1">
      <div className="schedule-header dead-space"></div>
    </div>
    {days.map(day => 
      <Day
        {...day}
      />
    )}
  </div>
)

DaysRow.propTypes = {
  days: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string.isRequired,
    num: PropTypes.number.isRequired,
    isToday: PropTypes.bool.isRequired
  }).isRequired).isRequired
}

export default DaysRow
