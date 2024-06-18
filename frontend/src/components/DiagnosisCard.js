import React from 'react'
import '../styles/DiagnosisCard.css'


export default function DiagnosisCard({ name, purpose }) {
  return (
    <div className='rectangle'>
          <div className='frame-2'>
            <div className='frame-3'>
              <div className='test-frame'>
                <span className='test-name'>
                {name}
                </span>
              </div>
            </div>
            <button className='badge-frame'>
              <div className='badge'>
                <span className='urgent'>Urgent</span>
              </div>
            </button>
          </div>
          <span className='purpose'>
            {purpose}
          </span>
        </div>
  );
}
