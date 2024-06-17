import React from 'react'
import "../styles/Symptom.css"
import { useState } from 'react'


function Symptom({symptom}) {

const [isSelected, setIsSelected] = useState(false);

  // Step 2: Handle button click
  const handleButtonClick = () => {
    setIsSelected(prevState => !prevState);
  };

  return (
    <div>
         <button 
        className={`symptom-button ${isSelected ? 'selected' : ''}`} 
        onClick={handleButtonClick}
      >
        <span className='symptom'> 
          {symptom}
        </span>
    </button>
    </div>
  )
}

export default Symptom