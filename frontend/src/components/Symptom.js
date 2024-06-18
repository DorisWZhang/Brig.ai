import React, { useState, useEffect, useRef } from 'react';
import "../styles/Symptom.css";

function Symptom({ symptom, innerRef }) {
  const [isSelected, setIsSelected] = useState(false);

  // Step 2: Handle button click
  const handleButtonClick = () => {
    setIsSelected(prevState => !prevState);
  };

  useEffect(() => {
    if (innerRef) {
      innerRef.current = { element: ref.current, isSelected };
    }
  }, [isSelected, innerRef]);

  const ref = useRef();

  return (
    <div>
      <button
        ref={ref}
        className={`symptom-button ${isSelected ? 'selected' : ''}`}
        onClick={handleButtonClick}
      >
        <span className='symptom'>
          {symptom}
        </span>
      </button>
    </div>
  );
}

export default Symptom;
