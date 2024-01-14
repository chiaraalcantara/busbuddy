import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Map from './pages/Map/Map';
import BusRegistration from './pages/BusRegistration/BusRegistration';

function App() {

  return (
    <>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            {/* <Route path="/" element={<Home />} /> */}
            <Route path="/map" element={<Map />} />
            <Route path="/bus-register" element={<BusRegistration />} />
          </Routes>
        </div>
      </Router>
    </>
  )
}

export default App;
