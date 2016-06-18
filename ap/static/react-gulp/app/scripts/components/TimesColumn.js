import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'

class TimesColumn extends Component {
  render() {
    var times = [];
    for (var i = 6; i < 24; i++) {
      var hour = "";
      if (i < 13) {
        hour += i.toString() + " AM";
      } else {
        var j = i - 12
        hour += j.toString() + " PM";
      }

      times.push(
        <div key={i} className="hour">
          <div className="hour-text" id={i}>{hour}</div>
        </div>
      );
    }
    return (
      <div className="col-md-2 col-xs-2 timebar">
        {times}
      </div>
    );
  }
}

export default connect()(TimesColumn);