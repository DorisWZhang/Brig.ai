import React from 'react'
import '../styles/DiagnosisCard.css'


export default function DiagnosisCard({ name, purpose }) {
  return (
    <div className='rectangle'>
          <div className='frame-2'>
            <div className='frame-3'>
              <div className='frame-4'>
                <span className='test-name'>
                  {name}
                </span>
              </div>
            </div>
            <button className='frame-5'>
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
