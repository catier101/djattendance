import React, { PropTypes } from 'react'
import { Button, Collapse, OverlayTrigger, Popover } from 'react-bootstrap'
import SelectedEvent from './SelectedEvent'
import RollSlipForm from './RollSlipForm'
import GroupLeaveSlipForm from './GroupLeaveSlipForm'

const ActionBar = ({submitRollShow, submitLeaveSlipShow, submitGroupLeaveSlipShow, otherReasonsShow,
                    selectedEvents, formSuccess, trainee, isSecondYear, tas, lsdShow,
                    toggleSubmitRoll, toggleSubmitLeaveSlip, toggleSubmitGroupLeaveSlip, toggleOtherReasons,
                    removeSelectedEvent, removeAllSelectedEvents, postRollSlip, postGroupLeaveSlip }) => {
  var disabledClass = 'remove-all';
  if (selectedEvents.length == 0) {
    disabledClass += ' disabled'
  }

  var hideRoll = {};
  if (trainee.terms_attended[trainee.terms_attended.length-1] <= 2) {
    hideRoll = {display: "none"};
  }

  return (
    <div style={{marginBottom: "10px"}}>
    {/*Form control buttons*/}
      <div>
        <Button className="action-button" onClick={toggleSubmitRoll} style={hideRoll} disabled={lsdShow}>Roll</Button>
        <Button className="action-button" onClick={toggleSubmitLeaveSlip}>Leave Slip</Button>
        <Button className="action-button" style={{display: "none"}} onClick={toggleSubmitGroupLeaveSlip}>Group Leave Slip</Button>
      </div>
    {/*Sessions selected*/}
      <div>
        <Collapse in={(selectedEvents.length > 0 || submitRollShow || submitLeaveSlipShow) && (!lsdShow)}>
          <div className="form-body">
            <div className="form-section">
              <div className="toggle-title">
                Sessions Selected
                <Button bsSize="small" className={disabledClass} onClick={removeAllSelectedEvents}>Remove All</Button>
              </div>
              <div>
                {selectedEvents.map(function(ev) {
                  return <SelectedEvent
                            {...ev}
                            onClick={() => removeSelectedEvent(ev)}
                            selectedEvents={selectedEvents}
                          />
                })}
              </div>
            </div>
          </div>
        </Collapse>
      </div>
    {/*Roll and slip form*/}
      <div>
        <RollSlipForm
          post={(rollSlip) => postRollSlip(rollSlip, selectedEvents, null)}
          submitRollShow={submitRollShow}
          submitLeaveSlipShow={submitLeaveSlipShow}
          toggleSubmitLeaveSlip={() => toggleSubmitLeaveSlip()}
          toggleOtherReasons={() => toggleOtherReasons()}
          otherReasonsShow={otherReasonsShow}
          tas={tas}
          selectedEvents={selectedEvents}
          isSecondYear={isSecondYear}
          isSlipDetail={false}
          lsdShow={lsdShow}
        />
      </div>
    {/*Group slip form*/}
      <div>
        <GroupLeaveSlipForm
          post={(groupLeaveSlip) => postGroupLeaveSlip(groupLeaveSlip, selectedEvents)}
          submitGroupLeaveSlipShow={submitGroupLeaveSlipShow}
          toggleSubmitGroupLeaveSlip={() => toggleSubmitGroupLeaveSlip()}
          toggleOtherReasons={() => toggleOtherReasons()}
          otherReasonsShow={otherReasonsShow}
          selectedEvents={selectedEvents}
          tas={tas}
          initialValues={{informStatus: "true"}}
        />
      </div>
    </div>
  )
}

ActionBar.propTypes = {
  submitRollShow: PropTypes.bool.isRequired, 
  submitLeaveSlipShow: PropTypes.bool.isRequired, 
  submitGroupLeaveSlipShow: PropTypes.bool.isRequired,
  selectedEvents: PropTypes.arrayOf(PropTypes.object.isRequired).isRequired,
  toggleSubmitRoll: PropTypes.func.isRequired, 
  toggleSubmitLeaveSlip: PropTypes.func.isRequired, 
  toggleSubmitGroupLeaveSlip: PropTypes.func.isRequired
}

export default ActionBar
