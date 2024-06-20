import React from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Question from './pages/Question';
import Results from './pages/Results'
import Landing from "./pages/Landing"
import FillQuestion from "./pages/FillQuestion"
import LocatePainQuestion from "./pages/LocatePainQuestion"
import PainQuestion from "./pages/PainQuestion"


function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />}></Route>
          <Route path="/questionnaire" element={<Question />}></Route>
          <Route path="/results" element={<Results />}></Route>
          <Route path="/fillq" element={<FillQuestion />}></Route>
          <Route path='/locatepainq' element={<LocatePainQuestion/>}></Route>
          <Route path='/painq' element={<PainQuestion/>}></Route>
        </Routes>
      </Router>
    </div>
  )
}

export default App