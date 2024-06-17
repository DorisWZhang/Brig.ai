import React from 'react'
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Question from './pages/Question';
import Results from './pages/Results'
import Landing from "./pages/Landing"




function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Question/>}></Route>
          <Route path="/" element={<Question/>}></Route>
          <Route path="/results" element ={<Results/>}></Route>
        </Routes>
      </Router>
    </div>
  )
}

export default App