import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import './App.css';


function App() {

  return (
    <>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            {/* <Route path="/" element={<Home />} /> */}
            {/* <Route path="/map" element={<Map />} /> */}
            {/* <Route path="/register" element={<Register />} /> */}
          </Routes>
        </div>
      </Router>
    </>
  )
}

export default App;
