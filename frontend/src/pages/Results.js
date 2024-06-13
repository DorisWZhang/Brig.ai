import React from 'react';
import '../styles/Results.css';
import { FaArrowLeft } from "react-icons/fa6";
import DiagnosisCard from "../components/DiagnosisCard"
import GeneratedQuestion from '../components/GeneratedQuestion';
import { GeneratedQuestionsList } from '../helpers/GeneratedQuestions';
import { useParams } from 'react-router-dom';
import Chatbot from "../components/Chatbot"


export default function Results() {

  

  return (
    <div className='main-container'>
      <div className='frame'>
        <div className='frame-1'>
          <button className='button-medium'>
              <FaArrowLeft/>
          </button>
        </div>
        <span className='back'>Back</span>
      </div>
      <div className='flex-row-eb'>
        <DiagnosisCard/>
        <div className='frame-6'>
          <div className='frame-7'>
            <div className='frame-8'>
              <div className='frame-9'>
                <div className='frame-a'>
                  <span className='pelvic-exam'>Pelvic Exam</span>
                </div>
              </div>
              <button className='button-frame'>
                <div className='badge-b'>
                  <span className='urgent-c'>Urgent</span>
                </div>
              </button>
            </div>
            <span className='check-growth-d'>
              Check for cysts, fibroid tumors, or other growths.
            </span>
          </div>
        </div>
      </div>
      <div className='frame-e'>

        <div className='gen-questions'>
          {GeneratedQuestionsList.map((question, idx) => {
            return (
              <GeneratedQuestion id = {idx} question={question.question}/>
            );
          })}
        </div>

        <div className='chatbot'>
          <Chatbot/>
        </div>

      </div>
    </div>
  );
}
