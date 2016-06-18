import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { Button, Collapse } from 'react-bootstrap'
import RollDetail from './RollDetail'
import LeaveSlipList from './LeaveSlipList'
import DropdownArrow from './DropdownArrow'

const AttendanceDetails = ({ unexcusedAbsences, unexcusedTardies, excused, slips, selectedEvents, tas,
                              unexcusedAbsencesShow, unexcusedTardiesShow, excusedShow, leaveSlipsShow, leaveSlipDetailsShow, otherReasonsShow,
                              onAbsencesToggle, onTardiesToggle, onExcusedToggle, toggleLeaveSlips, toggleLeaveSlipDetail, toggleOtherReasons,
                              removeAllSelectedEvents, removeSelectedEvent, postRollSlip, deleteSlip }) => {

  return (
    <div style={{margin: "15px 0px 40px 10px"}}>
      <div className="toggle-title">
        <span onClick={onAbsencesToggle}>
          <span className="toggle-title-text">Unexcused Absences ({unexcusedAbsences.length})</span>
          <DropdownArrow
            directionBoolean={unexcusedAbsencesShow}
          />
        </span>
        <Collapse in={unexcusedAbsencesShow}>
          <div>
            {unexcusedAbsences.map(ua =>
              <RollDetail
                {...ua}
              />
            )}
          </div>
        </Collapse>
      </div>
      <div className="toggle-title">
        <span onClick={onTardiesToggle}>
          <span className="toggle-title-text">Unexcused Tardies ({unexcusedTardies.length})</span>
          <DropdownArrow
            directionBoolean={unexcusedTardiesShow}
          />
        </span>
        <Collapse in={unexcusedTardiesShow}>
          <div>
            {unexcusedTardies.map(ut =>
              <RollDetail
                {...ut}
              />
            )}
          </div>
        </Collapse>
      </div>
      <div className="toggle-title">
        <span onClick={onExcusedToggle}>
          <span className="toggle-title-text">Excused ({excused.length})</span>
          <DropdownArrow
            directionBoolean={excusedShow}
          />
        </span>
        <Collapse in={excusedShow}>
          <div>
            {excused.map(e =>
              <RollDetail
                {...e}
              />
            )}
          </div>
        </Collapse>
      </div>
      <div className="toggle-title">
        <span onClick={toggleLeaveSlips}>
          <span className="toggle-title-text">Leave Slip History</span>
          <DropdownArrow
            directionBoolean={leaveSlipsShow}
          />
        </span>
        <LeaveSlipList
          slips={slips}
          leaveSlipsShow={leaveSlipsShow}
          leaveSlipDetailsShow={leaveSlipDetailsShow}
          onDetailClick={(id, evs, slipType, TA, comments, informed) => toggleLeaveSlipDetail(id, evs, slipType, TA, comments, informed)}
          removeAllSelectedEvents={() => removeAllSelectedEvents()}
          removeSelectedEvent={(ev) => removeSelectedEvent(ev)}
          postRollSlip={(rollSlip, selectedEvents, slipId) => postRollSlip(rollSlip, selectedEvents, slipId)}
          deleteSlip={(slipId) => deleteSlip(slipId)}
          toggleOtherReasons={() => toggleOtherReasons()}
          otherReasonsShow={otherReasonsShow}
          selectedEvents={selectedEvents}
          tas={tas}
        />
      </div>
    </div>
  )
}

AttendanceDetails.propTypes = {
  unexcusedAbsences: PropTypes.arrayOf(PropTypes.object.isRequired).isRequired,
  unexcusedAbsencesShow: PropTypes.bool.isRequired,
  unexcusedTardiesShow: PropTypes.bool.isRequired,
  excusedShow: PropTypes.bool.isRequired,
  onAbsencesToggle: PropTypes.func.isRequired,
  onTardiesToggle: PropTypes.func.isRequired,
  onExcusedToggle: PropTypes.func.isRequired
};

export default AttendanceDetails