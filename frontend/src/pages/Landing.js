import React from 'react'
import "../styles/Landing.css"

function Landing() {
  return (
    <div className='landing'>
      <div className='proj-title'>
        Brig.ai
      </div>
      <div className='through-line'>
      Preventing diagnostic delay for Endometriosis and PCOS by informing women of their most effective diagnostic tests based on their symptoms. Brig.ai bridges the gap between medical professionals and patients.
      </div>
        <a href="/questionnaire">
  <button className='start-button'>Get started</button>
</a>
    </div>
  )
}

export default Landing