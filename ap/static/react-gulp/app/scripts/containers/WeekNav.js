import { connect } from 'react-redux'
import { nextWeek, prevWeek, prevPeriod, nextPeriod } from '../actions'
import WeekBar from '../components/WeekBar'
import { TERM_START } from '../constants'

const mapStateToProps = (state) => {
  var startDate = dateFns.startOfWeek(state.reducer.date, {weekStartsOn: 1}),
      endDate = dateFns.endOfWeek(state.reducer.date, {weekStartsOn: 1})

  var difference = dateFns.differenceInWeeks(startDate, TERM_START);
  var period = Math.floor(difference/2);

  var firstStart = null;
  var firstEnd = null;
  var secondStart = null;
  var secondEnd = null;
  var isFirst = null;

  if (difference % 2 == 1) {
    secondStart = startDate;
    secondEnd = endDate;
    firstStart = dateFns.addDays(startDate, -7);
    firstEnd = dateFns.addDays(endDate, -7);
    isFirst = false;
  } else {
    firstStart = startDate;
    firstEnd = endDate;
    secondStart = dateFns.addDays(startDate, 7);
    secondEnd = dateFns.addDays(endDate, 7);
    isFirst = true;
  }

  return {
    isFirst: isFirst,
    firstStart: dateFns.format(firstStart, 'M/D'),
    firstEnd: dateFns.format(firstEnd, 'M/D'),
    secondStart: dateFns.format(secondStart, 'M/D'),
    secondEnd: dateFns.format(secondEnd, 'M/D'),
    period: period
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onPrevWeek: () => {
      dispatch(prevWeek())
    },
    onNextWeek: () => {
      dispatch(nextWeek())
    },
    onPrevPeriod: () => {
      dispatch(prevPeriod())
    },
    onNextPeriod: () => {
      dispatch(nextPeriod())
    }
  }
}

const WeekNav = connect(
  mapStateToProps,
  mapDispatchToProps
)(WeekBar)

export default WeekNav