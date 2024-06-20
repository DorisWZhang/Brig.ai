import React from 'react';
import '../styles/DiagnosisCard.css';

export default function DiagnosisCard({ name, explanation, showUrgentBadge }) {
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
        {showUrgentBadge && (
          <button className='badge-frame'>
            <div className='badge'>
              <span className='urgent'> 
                Urgent
              </span>
            </div>
          </button>
        )}
      </div>
      <div className='card-text'>
        <span className='purpose'>
          {explanation}
        </span>
      </div>
    </div>
  );
}
