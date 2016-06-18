import React, { Component, PropTypes } from 'react'

export default class Trainee extends Component {
  render() {
    return (
      <div>
        <h2>{this.props.trainee.name}&#39;s Schedule</h2>
      </div>
    )
  }
}
