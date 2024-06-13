
import React from 'react';
import "../styles/GeneratedQuestion.css"

export default function GeneratedQuestion({question}) {
  return (
    <button className='q-button'>
        <span className='gen-q'> {question} </span>
    </button>
  );
}