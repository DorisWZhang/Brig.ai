import React from 'react'
import "../styles/Question.css"


function Question({question, symptoms}) {
  return (
    <div className='main-container'>
        <div className='frame'>
          <div className='back'>Back button</div>
          <div className='frame-4'>
            <span className='symp-question'>
              {question} DO U HV PAIN
            </span>
            <div className='frame-5'>
              {symptoms}
            </div>
          </div>
          <div className='button-frame'>
          <button className='continue-button'>
            Continue
          </button>
          </div>
        </div>
    </div>
  )
}

export default Question
