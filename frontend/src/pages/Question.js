import React, { useState } from 'react';
import "../styles/Question.css";
import { Link, useNavigate } from 'react-router-dom';
import { QuestionList } from '../helpers/Questionnaire';
import Symptom from "../components/Symptom";

function Question({}) {

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const navigate = useNavigate();
  const question = QuestionList[currentQuestionIndex];
  const symptoms = [];

 

  const handleContinueClick = () => {
    if (currentQuestionIndex < QuestionList.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      navigate('/results', { state: { questionList: QuestionList } });
    }
  };

  const handleBackClick = () => {
    if (currentQuestionIndex === 0) {
      navigate('/');
    } else {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  return (
    <div className='question-screen'>
      <div className='frame'>
        <button className='back' onClick={handleBackClick}>Back</button>
        <div className='frame-4'>
          <span className='symp-question'>
            {question.question}
          </span>
          <div className='symp-1'>
            {question.symptoms.slice(0, 5).map((symptom, index) => (
              <Symptom key={index} symptom={symptom} />
            ))}
          </div>
          {question.symptoms.length > 5 && (
            <div style={{ display: 'flex' }} className='symp-2'>
              {question.symptoms.slice(5).map((symptom, index) => (
                <Symptom key={index} symptom={symptom} />
              ))}
            </div>
          )}
        </div>
        <div className='button-frame'>
          <button className='continue-button' onClick={handleContinueClick}>
            {currentQuestionIndex < QuestionList.length - 1 ? 'Continue' : 'View your Results'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Question;
