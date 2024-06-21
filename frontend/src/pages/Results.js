import React from 'react';
import '../styles/Results.css';
import { FaArrowLeft } from "react-icons/fa6";
import DiagnosisCard from "../components/DiagnosisCard";
import GeneratedQuestion from '../components/GeneratedQuestion';
import { GeneratedQuestionsList } from '../helpers/GeneratedQuestions';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Chatbot from "../components/Chatbot";
import { DiagnosticGroups } from '../helpers/DiagnosticGroup';
import Logo from "../assets/photos/brig.png"

export default function Results() {
  const navigate = useNavigate();
  const location = useLocation();
  const { data } = location.state || { data: {} };
  console.log(data); // For debugging purposes

  const endo = data['endo_severity'];
  const endoCluster = data['endo_cluster'];
  const pcos = data['pcos_severity'];
  const pcosCluster = data['pcos_cluster'];

  const endoDiagnosticGroup = endo > 0.5 ? DiagnosticGroups.find(group => group.ID === `Endo Cluster ${endoCluster}`) : null;
  const pcosDiagnosticGroup = pcos > 0.5 ? DiagnosticGroups.find(group => group.ID === `PCOS Cluster ${pcosCluster}`) : null;

  const finalEndoDiagnosticGroup = endo > 0.5 && endoDiagnosticGroup && endoDiagnosticGroup.ID === "Endo Cluster 0"
    ? DiagnosticGroups.find(group => group.ID === `Endo Cluster 1`)
    : endoDiagnosticGroup;

  const finalPcosDiagnosticGroup = pcos > 0.5 && pcosDiagnosticGroup && pcosDiagnosticGroup.ID === "PCOS Cluster 0"
    ? DiagnosticGroups.find(group => group.ID === `PCOS Cluster 1`)
    : pcosDiagnosticGroup;

  const diagnosticTests = [
    ...(finalEndoDiagnosticGroup ? finalEndoDiagnosticGroup.tests : []),
    ...(finalPcosDiagnosticGroup ? finalPcosDiagnosticGroup.tests : [])
  ];

  // Remove duplicates based on the test name
  const uniqueDiagnosticTests = Array.from(new Set(diagnosticTests.map(test => test.name)))
    .map(name => diagnosticTests.find(test => test.name === name));

  let message = '';
  if (endo > pcos && endo > 0.5) {
    message = finalEndoDiagnosticGroup ? finalEndoDiagnosticGroup.message : '';
  } else if (pcos > endo && pcos > 0.5) {
    message = finalPcosDiagnosticGroup ? finalPcosDiagnosticGroup.message : '';
  }

  const handleBackClick = () => {
    navigate("/");
  };

  const showUrgentBadge = endo > 0.8 || pcos > 0.8;

  return (
    <div className='main'>
      <div className='main-frame'>
          <button className='button-medium' onClick={handleBackClick}>
            <FaArrowLeft />
          </button>
      
        
        <span className='back-to-qs'>Back</span>
        
      
      </div>
      <img src={Logo} className='corner-logo-results'/>
      <div className='message'>
        {message || 'No specific diagnostic tests recommended based on the provided data.'}
      </div>
      <div className='flex-row-eb'>
        {uniqueDiagnosticTests.map((test, idx) => (
          <DiagnosisCard
            key={idx}
            id={idx}
            name={test.name}
            explanation={test.explanation}
            showUrgentBadge={showUrgentBadge} // Pass the prop to DiagnosisCard
          />
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
          All recommended diagnosis tools must be administered and discussed with a licensed medical professional. Brig.ai can make mistakes.
        </div>
      </div>
    </div>
  );
}
