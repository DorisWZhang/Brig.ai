import React from 'react'
import "../styles/Landing.css"
import Logo from "../assets/photos/brig.png"

function Landing() {
  return (
    <div className='landing'>
      <div className='proj-title'>
        <img src={Logo} className='logo'/>
       
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