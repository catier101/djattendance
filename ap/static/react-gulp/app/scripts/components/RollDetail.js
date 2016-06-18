import React, { PropTypes } from 'react'
import { Well } from 'react-bootstrap'

const RollDetail = ({ event, slip, roll }) => {


  return (
    <div className="row details">
      <div className="col-md-7 col-xs-6">
        {dateFns.format(event['start'], 'M/D ddd')}
      </div>
      <div className="col-md-17 col-xs-18">
        {event["name"]}
      </div>
    </div>
  )
}

RollDetail.propTypes = {
  event: PropTypes.object.isRequired,
  slip: PropTypes.object.isRequired,
  roll: PropTypes.object.isRequired
}

export default RollDetail