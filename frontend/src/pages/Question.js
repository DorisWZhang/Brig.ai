import React, { useState, useEffect } from 'react';
import "../styles/Question.css";
import { useNavigate } from 'react-router-dom';
import { QuestionList } from '../helpers/Questionnaire';
import Symptom from "../components/Symptom";
import Logo from "../assets/photos/brig.png"

function Question() {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const navigate = useNavigate();
  const question = QuestionList[currentQuestionIndex]; /* the question on page */

  // State to track selected symptoms across all pages
  const [selectedSymptoms, setSelectedSymptoms] = useState({});

  // State to track selected symptoms for the current page only
  const [currentPageSymptoms, setCurrentPageSymptoms] = useState({});

  // Update selected symptoms for current page
  const updateSelectedSymptoms = (symptomId, isSelected) => {
    setCurrentPageSymptoms(prevState => ({
      ...prevState,
      [symptomId]: isSelected ? 1 : 0 // Convert true/false to 1/0
    }));
  };

  // Reset current page symptoms to empty
  const resetCurrentPageSymptoms = () => {
    setCurrentPageSymptoms({});
  };

  // Save symptoms to server
  const saveSymptoms = () => {
    fetch('http://127.0.0.1:5000/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(currentPageSymptoms)
    })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  // Handle click to continue to next question or view results
  const handleContinueClick = () => {
    saveSymptoms(); // Save current page symptoms
    resetCurrentPageSymptoms(); // Reset current page symptoms

    // Navigate to the next question or results page
    if (currentQuestionIndex < QuestionList.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      navigate('/painq');
    }
  };

  // Handle click to go back to previous question
  const handleBackClick = () => {
    if (currentQuestionIndex === 0) {
      navigate('/');
    } else {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  useEffect(() => {
    // Merge currentPageSymptoms into selectedSymptoms after each update
    setSelectedSymptoms(prevState => ({
      ...prevState,
      ...currentPageSymptoms
    }));
  }, [currentPageSymptoms]);

  return (
    <div className='question-screen'>
      <div className='frame'>
        <button className='back' onClick={handleBackClick}>Back</button>
        <img src={Logo} className='corner-logo'/>
        <div className='frame-4'>
          <span className='symp-question'>
            {question.question}
          </span>
          <div className='symp-1'>
            {question.symptoms.slice(0, 5).map((symptom, index) => (
              <Symptom
                key={index}
                symptom={symptom}
                isSelected={currentPageSymptoms[symptom.id] === 1}
                updateSelected={updateSelectedSymptoms}
              />
            ))}
          </div>
          {question.symptoms.length > 5 && (
            <div style={{ display: 'flex' }} className='symp-2'>
              {question.symptoms.slice(5).map((symptom, index) => (
                <Symptom
                  key={index + 5}
                  symptom={symptom}
                  isSelected={currentPageSymptoms[symptom.id] === 1}
                  updateSelected={updateSelectedSymptoms}
                />
              ))}
            </div>
          )}
        </div>
        <div className='button-frame'>
          <button className='continue-button' onClick={handleContinueClick}>
            {'Continue'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Question;
