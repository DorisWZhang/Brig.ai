import React from 'react';
import '../styles/Results.css';
import { FaArrowLeft } from "react-icons/fa6";
import DiagnosisCard from "../components/DiagnosisCard"
import GeneratedQuestion from '../components/GeneratedQuestion';
import { GeneratedQuestionsList } from '../helpers/GeneratedQuestions';
import { useParams } from 'react-router-dom';
import Chatbot from "../components/Chatbot"
import { DiagnosisList } from '../helpers/DiagnosticTests';

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
        {DiagnosisList.map((test, idx) =>{
          return (    
            <DiagnosisCard id={idx} name={test.name} purpose={test.purpose}/>
          );
        })}
        
      </div>
      <div className='frame-e'>
        <div className='gen-questions'>
          {GeneratedQuestionsList.map((question, idx) => {
            return (
              <GeneratedQuestion id = {idx} question={question.question}
              icon={question.icon}/>
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
