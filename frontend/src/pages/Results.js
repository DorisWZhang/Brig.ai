import React from 'react';
import '../styles/Results.css';
import { FaArrowLeft } from "react-icons/fa6";
import DiagnosisCard from "../components/DiagnosisCard"
import GeneratedQuestion from '../components/GeneratedQuestion';
import { GeneratedQuestionsList } from '../helpers/GeneratedQuestions';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Chatbot from "../components/Chatbot"
import { DiagnosisList } from '../helpers/DiagnosticTests';

export default function Results() {
  const navigate = useNavigate();
  const location = useLocation();
  const { questionList } = location.state || { questionList: [] };

  const handleBackClick = () => {
    navigate("/");
  };

  return (
    <div className='main'>
      <div className='main-frame'>
        <div className='frame-1'>
          <button className='button-medium' onClick={handleBackClick}>
            <FaArrowLeft />
          </button>
        </div>
        <span className='back-to-qs'>Back</span>
      </div>
      <div className='message'>
        Based on your symptoms, here are the diagnostic tests you may want to seek out. 
      </div>
      <div className='flex-row-eb'>
        {DiagnosisList.map((test, idx) => (
          <DiagnosisCard key={idx} id={idx} name={test.name} purpose={test.purpose} />
        ))}
      </div>
      <div className='frame-e'>
        <div className='gen-questions'>
          {GeneratedQuestionsList.map((question, idx) => (
            <GeneratedQuestion key={idx} id={idx} question={question.question} icon={question.icon} />
          ))}
        </div>
        <div className='chatbot'>
          <Chatbot />
        </div>
        <div className='note'>
          All recommended diagnosis tools must be administered and discussed with a licensed medical professional. 
        </div>
      </div>
    </div>
  );
}
