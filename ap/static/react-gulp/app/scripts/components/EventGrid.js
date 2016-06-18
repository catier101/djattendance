import React, { PropTypes } from 'react'
import EventColumn from './EventColumn'

import { joinValidClasses } from '../constants'

const EventGrid = ({eventsByDay, selectedEvents, onEventClick, onHeaderClick}) => {
  var k = 0;
  return (
    <div>
      {eventsByDay.map(daysEsr =>
        <EventColumn
          key={k++}
          {...daysEsr}
          onEventClick={(ev) => onEventClick(ev)}
          onHeaderClick={(evs) => onHeaderClick(evs)}
          selectedEvents={selectedEvents}
        />
      )}
    </div>
  )
}

EventGrid.propTypes = {
  eventsByDay: PropTypes.arrayOf(PropTypes.object.isRequired).isRequired,
  onEventClick: PropTypes.func.isRequired
}

export default EventGrid
