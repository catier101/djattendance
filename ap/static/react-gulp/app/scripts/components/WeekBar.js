import React, { PropTypes } from 'react'

const WeekBar = ({isFirst, firstStart, firstEnd, secondStart, secondEnd, period,
                    onPrevWeek, onNextWeek, onPrevPeriod, onNextPeriod}) =>
(
  <div className="week-bar-container">
    <div className="btn-toolbar week-bar" role="toolbar">
      <div className="controls btn-group">
        <button className="btn btn-default clndr-previous-button no-margin" disabled={period == 0} onClick={onPrevPeriod}>&lt;</button>
        <button className="date-range btn btn-default no-margin" disabled={isFirst} onClick={onPrevWeek}>
          {firstStart} - {firstEnd}
        </button>
        <button className="date-range btn btn-default no-margin" disabled={!isFirst} onClick={onNextWeek}>
          {secondStart} - {secondEnd}
        </button>
        <button className="btn btn-default clndr-next-button" disabled={period == 9} onClick={onNextPeriod}>&gt;</button>
      </div>
    </div>
    <div className="period">
      PERIOD {period}
    </div>
  </div>
)

WeekBar.propTypes = {
  isFirst: PropTypes.bool.isRequired,
  firstStart: PropTypes.string.isRequired,
  firstEnd: PropTypes.string.isRequired,
  secondStart: PropTypes.string.isRequired,
  secondEnd: PropTypes.string.isRequired,
  onPrevWeek: PropTypes.func.isRequired,
  onNextWeek: PropTypes.func.isRequired,
  onPrevPeriod: PropTypes.func.isRequired,
  onNextPeriod: PropTypes.func.isRequired
};

export default WeekBar
