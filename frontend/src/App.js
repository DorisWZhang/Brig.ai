import React from 'react'
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Menstrual from './pages/endo questions/Menstrual';
import Results from './pages/Results'

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Results/>}>
          </Route>
        </Routes>
      </Router>
    </div>
  )
}

export default App