import { connect } from 'react-redux'
import { toggleEvent, toggleDaysEvents } from '../actions'
import EventGrid from '../components/EventGrid'
import { sortEsr } from '../constants'

/*
The data structure guide
GridContainer passes an array called cols to EventGrid
GridContainer -----cols[]-----> EventGrid

EventGrid uses .map to pass each object in cols[] to an EventColumn component
EventGrid -----dayEsr-----> EventColumn

dayEsr has a date object and a sorted array of esr's corresponding to the column meaning a particular day
The date object is used for the column header, .map is called on the sorted array to pass on esr objects to EventView

EventColumn -----esr-----> EventView
*/

const mapStateToProps = (state) => {
  var weekStart = dateFns.format(dateFns.startOfWeek(state.reducer.date, {weekStartsOn: 1}), 'M/D/YY'),
      weekEnd = dateFns.format(dateFns.endOfWeek(state.reducer.date, {weekStartsOn: 1}), 'M/D/YY');

  //get just this week's events
  var weekEventsSlipsRolls = _.filter(state.reducer.eventsSlipsRolls, function(esr) {
    return (new Date(weekStart) < new Date(esr.event['start']) && dateFns.addDays(weekEnd, 1) > new Date(esr.event['end']));
  }, this);

  //sort events by day of the week
  //esr stands for events, slips, rolls
  var cols = [];
  for (var i = 0; i < 7; i++) {
    var dayESR = _.filter(weekEventsSlipsRolls, function(esr) {
      return dateFns.getDay(esr.event['start']) === i;
    });

    var sorted = dayESR.sort(sortEsr);

    cols.push(
      {
        //have to do some funky business because dateFns.getDay returns LD as first but we want LD to be last
        date: dateFns.addDays(weekStart, i == 0 ? 6 : i - 1), 
        daysEsr: sorted
      }
    );
  }

  //move Lord's Day events to the end of the week
  var ld = cols.splice(0, 1);
  cols.push(ld[0]);

  return {
    eventsByDay: cols,
    selectedEvents: state.reducer.selectedEvents,
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onEventClick: (ev) => {
      dispatch(toggleEvent(ev))
    },
    onHeaderClick: (evs) => {
      dispatch(toggleDaysEvents(evs))
    }
  }
}

const GridContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(EventGrid)

export default GridContainer