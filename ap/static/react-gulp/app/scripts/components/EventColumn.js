import React, { PropTypes } from 'react'
import EventView from './EventView'

const EventColumn = ({daysEsr, date, selectedEvents, onEventClick, onHeaderClick}) => {
  var header = dateFns.format(date, 'ddd D');
  var todayStyle = {};
  if (dateFns.isSameDay(date, new Date())) {
    todayStyle = {
      backgroundColor: "#dff0d8",
      border: "solid thin #ccc",
      top: "-23px"
    };
  }
  var daysEvents = [];
  for (var i = 0; i < daysEsr.length; i++) {
    daysEvents.push(daysEsr[i].event);
  }

  var k = 0;
  return (
    <div className="day event-col col-md-3 col-xs-3 no-padding">
      <div className="days-row" style={todayStyle} onClick={() => onHeaderClick(daysEvents)}>
        {header}
      </div>
      {daysEsr.map(function(esr) {
        if (esr) {
          return <EventView 
                    key={k++}
                    {...esr} 
                    onClick={() => onEventClick(esr.event)}
                    selectedEvents={selectedEvents}
                  />
        }
      })}
    </div>
  )
}

EventColumn.PropTypes = {
  daysEsr: PropTypes.arrayOf(PropTypes.shape({
    event: PropTypes.object.isRequired,
    roll: PropTypes.object.isRequired,
    slip: PropTypes.object.isRequired,
  }).isRequired).isRequired,
  selectedEvents: PropTypes.arrayOf(PropTypes.object.isRequired).isRequired,
  onEventClick: PropTypes.func.isRequired
}

export default EventColumn