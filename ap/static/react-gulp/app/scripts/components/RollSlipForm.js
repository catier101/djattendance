import React, { Component, PropTypes } from 'react'
import { Button, Collapse, OverlayTrigger, Popover } from 'react-bootstrap'
import { reduxForm } from 'redux-form'
import initialState from '../initialState'
import { postLeaveSlip } from '../actions'
export const fields = [ 'rollStatus', 'slipType', 'comments', 'informed', 'TAInformed' ]

const validate = (values, props) => {
  var ta_names = [];
  for (var i = 0; i < initialState.reducer.tas.length; i++) {
    ta_names.push(initialState.reducer.tas[i].firstname + ' ' + initialState.reducer.tas[i].lastname);
  }
  const errors = {}
  if (props.submitLeaveSlipShow && values.informed == "true" && !ta_names.includes(values.TAInformed)) {
    errors.TAInformed = 'No TA selected';
  }
  if (props.submitLeaveSlipShow && !values.slipType) {
    errors.slipType = 'No reason selected';
  } 
  return errors
}

//forms use the redux-form library
//http://redux-form.com/
const RollSlipForm = ({fields: { rollStatus, slipType, comments, informed, TAInformed }, handleSubmit, resetForm, 
                    submitRollShow, submitLeaveSlipShow, otherReasonsShow, toggleSubmitLeaveSlip, toggleOtherReasons,
                    submitting, post, deleteSlip, tas, status, selectedEvents, isSecondYear, isSlipDetail, lsdShow}) => {
  var disable = true;
  if (status == "P" || status === undefined) {
    disable = false;
  }

  var hideDelete = null;
  if (status === undefined) {
    hideDelete = {display: "none"};
  }

  return (
    <form onSubmit={handleSubmit(post)}>
      <div className="position-container">
        <Collapse in={submitRollShow && isSecondYear && !isSlipDetail}>
          <div className="form-body form-together">
            <div className="form-section">
              <div className="toggle-title">Enter Roll</div>
              <div style={{width: "100%", paddingBottom: "30px"}}>
                <label className="radio-input">
                  <input type="radio" {...rollStatus} value="P" checked={rollStatus.value === "P"} name="status" /> Present
                </label>
                <label className="radio-input">
                  <input type="radio" {...rollStatus} value="A" checked={rollStatus.value === "A"} name="status" /> Absent
                </label>
                <label className="radio-input">
                  <input type="radio" {...rollStatus} value="T" checked={rollStatus.value === "T"} name="status" /> Tardy
                </label>
                <label className="radio-input">
                  <input type="radio" {...rollStatus} value="U" checked={rollStatus.value === "U"} name="status" /> Uniform
                </label>
                <label className="radio-input">
                  <input type="radio" {...rollStatus} value="L" checked={rollStatus.value === "L"} name="status" /> Left Class
                </label>
              </div>
              <div onClick={toggleSubmitLeaveSlip} className="checkbox-container leaveslip-checkbox">
                <input type="checkbox" checked={submitLeaveSlipShow}/> Leave Slip
              </div>
            </div>
          </div>
        </Collapse>
        <Collapse in={submitLeaveSlipShow && !lsdShow}>
          <div className="form-body form-together bottom-padding-25">
            <div className="form-section">
              <div className="toggle-title">Reason</div>
              <div>
                <div className="reason-container">
                  <label className="radio-input">
                    <input type="radio" {...slipType} name="reason" value="SICK" disabled={disable} checked={slipType.value === "SICK"}/> Sickness 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...slipType} name="reason" value="SERV" disabled={disable} checked={slipType.value === "SERV"}/> Service 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...slipType} name="reason" value="FWSHP" disabled={disable} checked={slipType.value === "FWSHP"}/> Fellowship 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...slipType} name="reason" value="NIGHT" disabled={disable} checked={slipType.value === "NIGHT"}/> Night Out 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...slipType} name="reason" value="MEAL" disabled={disable} checked={slipType.value === "MEAL"}/> Meal Out 
                  </label>
                  <span onClick={toggleOtherReasons} className="checkbox-container">
                    <input type="checkbox" disabled={disable} checked={otherReasonsShow}/> More <span className="caret"></span>
                  </span>
                  <Collapse in={otherReasonsShow}>
                    <div data-toggle="buttons">
                      <label className="radio-input">
                        <input type="radio" {...slipType} name="reason" value="INTVW" disabled={disable} checked={slipType.value === "INTVW"}/> Interview 
                      </label>
                      <label className="radio-input">
                        <input type="radio" {...slipType} name="reason" value="GOSP" disabled={disable} checked={slipType.value === "GOSP"}/> Gospel 
                      </label>
                      <label className="radio-input">
                        <input type="radio" {...slipType} name="reason" value="CONF" disabled={disable} checked={slipType.value === "CONF"}/> Conference 
                      </label>
                      <label className="radio-input">
                        <input type="radio" {...slipType} name="reason" value="WED" disabled={disable} checked={slipType.value === "WED"}/> Wedding 
                      </label>
                      <label className="radio-input">
                        <input type="radio" {...slipType} name="reason" value="FUNRL" disabled={disable} checked={slipType.value === "FUNRL"}/> Funeral 
                      </label>
                      <label className="radio-input">
                        <input type="radio" {...slipType} name="reason" value="SPECL" disabled={disable} checked={slipType.value === "SPECL"}/> Special 
                      </label>
                      <label className="radio-input" style={{width: "33%"}}>
                        <input type="radio" {...slipType} name="reason" value="OTHER" disabled={disable} checked={slipType.value === "OTHER"}/> Other 
                      </label>
                      <label className="radio-input" style={{width: "66%"}}>
                        <input type="radio" {...slipType} name="reason" value="EMERG" disabled={disable} checked={slipType.value === "EMERG"}/> Family Emergency 
                      </label>
                    </div>
                  </Collapse>
                </div>
                <div className="top-border">
                  <label className="notification-only">
                    <input type="radio" {...slipType} name="reason" value="NOTIF" disabled={disable} checked={slipType.value === "NOTIF"}/> Notification Only 
                  </label>
                </div>
                {slipType.touched && slipType.error && <div className="form-error">{slipType.error}</div>}
              </div>
              <div>
                <div className="toggle-title">Comments</div>
                <textarea className="comments-textarea" readOnly={disable}
                  {...comments}
                  defaultValue={comments.value || ''}
                />
              </div>
              <div className="position-container">
                <select className="form-control select-inform-status" {...informed} value={informed.value || ''} disabled={disable}>
                  <option value={"true"}>TA informed </option>
                  <option value={"false"}>Did not inform training office </option>
                  <option value="texted">Texted attendance number (for sisters during non-front office hours only)</option>
                </select>
                <span className="caret select-caret"></span>
              </div>
              <Collapse in={informed.value == "true"}>
                <div className="ta-names">
                  <label className="radio-input">
                    <input type="radio" {...TAInformed} name="ta" value="Andrew Li" disabled={disable} checked={TAInformed.value === "Andrew Li"}/> Andrew Li 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...TAInformed} name="ta" value="Jerome Keh" disabled={disable} checked={TAInformed.value === "Jerome Keh"}/> Jerome Keh 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...TAInformed} name="ta" value="Joseph Bang" disabled={disable} checked={TAInformed.value === "Joseph Bang"}/> Joseph Bang
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...TAInformed} name="ta" value="Paul Deng" disabled={disable} checked={TAInformed.value === "Paul Deng"}/> Paul Deng 
                  </label>
                  <label className="radio-input">
                    <input type="radio" {...TAInformed} name="ta" value="Walt Hale" disabled={disable} checked={TAInformed.value === "Walt Hale"}/> Walt Hale 
                  </label>
                </div>
              </Collapse>
              {TAInformed.touched && TAInformed.error && <div className="form-error">{TAInformed.error}</div>}
            </div>
          </div>
        </Collapse>
        <Collapse in={submitRollShow || submitLeaveSlipShow}>
          <div>
            <div className="delete-button">
              <Button disabled={disable} bsSize="xsmall" bsStyle="danger" style={hideDelete} onClick={deleteSlip}>
                Delete
              </Button>
            </div>
            <div className="form-buttons">
              <Button type="button" disabled={submitting || disable} onClick={resetForm} bsSize="xsmall" style={{marginRight: "3px"}}>
                Reset Form
              </Button>
              <Button type="submit" disabled={submitting || TAInformed.error ? true : false || slipType.error ? true : false || disable} bsStyle="primary" bsSize="xsmall">
                {submitting ? <i/> : <i/>} Submit
              </Button>
            </div>
          </div>
        </Collapse>
      </div>
    </form>
  )
}


RollSlipForm.propTypes = {
  fields: PropTypes.object.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  resetForm: PropTypes.func.isRequired,
  submitting: PropTypes.bool.isRequired,
  post: PropTypes.func.isRequired,
  toggleOtherReasons: PropTypes.func.isRequired
}

export default reduxForm({
  form: 'rollSlipForm',
  fields,
  validate
},
state => ({
  initialValues: state.reducer.leaveSlipDetailFormValues
}))(RollSlipForm)
