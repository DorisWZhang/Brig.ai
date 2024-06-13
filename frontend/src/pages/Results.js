import React from 'react';
import '../styles/Results.css';
import { FaArrowLeft } from "react-icons/fa6";
import DiagnosisCard from "../components/DiagnosisCard"
import GeneratedQuestion from '../components/GeneratedQuestion';

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
        <div className='frame-f'>


          <GeneratedQuestion/>


          <div className='frame-15'>
            <div className='user-speak-rounded'>
              <div className='flex-row-d'>
                <div className='vector-16' />
                <div className='vector-17' />
                <div className='vector-18' />
              </div>
              <div className='vector-19' />
            </div>
            <span className='transvaginal-ultrasound-1a'>
              What are my rights in asking for a transvaginal ultrasound?
            </span>
          </div>
        </div>
        <div className='frame-1b'>
          <button className='button'>
            <span className='intrusive-procedure'>
              Is this procedure intrusive?
            </span>
          </button>
          <button className='button-1c'>
            <div className='linear-medical-note'>
              <div className='vector-1d' />
            </div>
            <span className='need-test'>Why do I need this test?</span>
          </button>
        </div>
      </div>
      <div className='rectangle-1e'>
        <div className='frame-1f' />
        <span className='message-novi'>Message Novi</span>
      </div>
    </div>
  );
}
