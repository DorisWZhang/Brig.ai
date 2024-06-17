import React from 'react'
import "../styles/Question.css"
import{Link, useLocation} from 'react-router-dom';
import { QuestionList } from '../helpers/Questionnaire';
import Symptom from "../components/Symptom"
import { useParams } from 'react-router-dom';


/* Save the information, navigate to next question
*/
function clickContinue(){

}

function Question() {


  const { id } = useParams();
  const question = QuestionList[0];

  return (
    <div className='question-screen'>
        <div className='frame'>
          <Link className='back'> Back </Link>
          <div className='frame-4'>
            <span className='symp-question'>
              {question.question} 
            </span>
            <div className='symp-1'>
              {question.symptoms.slice(0,4).map((symptom, index) => {
                return (
                  <Symptom key={index} symptom={symptom} />
                );
              })}
            </div>
              {question.symptoms.length > 4 && (
                <div style={{ display: 'flex' }} className='symp-2'>
                  {question.symptoms.slice(4).map((symptom, index) => (
                    <Symptom key={index} symptom={symptom} />
                ))}
              </div>
                )}
          </div>
          
          <div className='button-frame'>
          <button className='continue-button'>
            Continue
          </button>
          </div>
        </div>
    </div>
  )
}

export default Question
