import React, { Component, PropTypes } from 'react'

import Trainee from '../components/Trainee'
import WeekNav from '../containers/WeekNav'
import GridContainer from '../containers/GridContainer'
import TimesColumn from '../components/TimesColumn'
import AttendanceDetails from '../containers/AttendanceDetails'
import AttendanceActions from '../containers/AttendanceActions'

const Attendance = () => (
  <div>
    <WeekNav />
    <div className="row">
      <div className="col-md-8">
        <AttendanceActions />
        <AttendanceDetails />
      </div>
      <div className="col-md-16 event-grid">
        <TimesColumn />
        <GridContainer />
      </div>
    </div>
  </div>
)

export default Attendance