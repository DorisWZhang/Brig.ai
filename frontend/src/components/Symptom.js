import React from 'react';
import "../styles/Symptom.css";

const Symptom = ({ symptom, isSelected, updateSelected }) => {
  const handleButtonClick = () => {
    const newSelected = !isSelected;
    updateSelected(symptom, newSelected);
  };

  return (
    <div>
      <button
        id={symptom} // Set the id to the symptom text
        className={`symptom-button ${isSelected ? 'selected' : ''}`}
        onClick={handleButtonClick}
      >
        <span className='symptom'>
          {symptom}
        </span>
      </button>
    </div>
  );
};

export default Symptom;
