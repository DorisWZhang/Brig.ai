import React from 'react'
import "../styles/Symptom.css"

function Symptom({symptom}) {
  return (
    <div>
        <button className='symptom-button'>
        <span className='symptom'> 
          {symptom}
        </span>
    </button>
    </div>
  )
}

export default Symptom