import React from 'react'
import '../styles/DiagnosisCard.css'

function DiagnosisCard() {
  return (
    <div className='rectangle'>
          <div className='frame-2'>
            <div className='frame-3'>
              <div className='frame-4'>
                <span className='transvaginal-ultrasound'>
                  Transvaginal Ultrasound
                </span>
              </div>
            </div>
            <button className='frame-5'>
              <div className='badge'>
                <span className='urgent'>Urgent</span>
              </div>
            </button>
          </div>
          <span className='check-growth'>
            Check for cysts, fibroid tumors, or other growths.
          </span>
        </div>
  )
}

export default DiagnosisCard