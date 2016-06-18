import React, { PropTypes } from 'react'

import { joinValidClasses } from '../constants'

const DropdownArrow = ({ directionBoolean }) => {
  var faClass = "fa fa-lg fa-angle-"
  if (directionBoolean) {
    faClass += "down";
  } else {
    faClass += "right";
  }

  return (
    <i className={faClass}></i>
  )
}

DropdownArrow.propTypes = {
  directionBoolean: PropTypes.bool.isRequired
}

export default DropdownArrow