import React, { PropTypes } from 'react'
import { Alert } from 'react-bootstrap'

const FormAlert = ({ formSuccess, handleAlertDismiss }) => {
  if (formSuccess === true) {
    return (
      <Alert bsStyle="success" onDismiss={handleAlertDismiss}>
        Submitted!
      </Alert>
    )
  }
  else if (formSuccess === false ) {
    return (
      <Alert bsStyle="danger" onDismiss={handleAlertDismiss}>
        Something went wrong try again
      </Alert>
    )
  }
  else {
    return (<span></span>)
  }
}

FormAlert.propTypes = {
  name: PropTypes.string.isRequired,
  num: PropTypes.string.isRequired,
  isToday: PropTypes.bool.isRequired
}

export default FormAlert