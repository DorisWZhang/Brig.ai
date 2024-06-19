import React from 'react';
import "../styles/Symptom.css";

const Symptom = ({ symptom, isSelected, updateSelected }) => {
  const handleButtonClick = () => {
    const newSelected = !isSelected;
    updateSelected(symptom.id, newSelected);
  };

  return (
    <div>
      <button
        id={symptom.id} // Set the id to the symptom id
        className={`symptom-button ${isSelected ? 'selected' : ''}`}
        onClick={handleButtonClick}
      >
        <span className='symptom'>
          {symptom.text}
        </span>
      </button>
    </div>
  );
};

export default Symptom;
