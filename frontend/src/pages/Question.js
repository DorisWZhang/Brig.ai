import React from 'react'
import "../styles/Question.css"


function Question({question, symptoms}) {
  return (
    <div className='main-container'>
      <div>
        {question}
      </div>

      <div className='symptoms'>
        
      </div>


    </div>
  )
}

export default Question
