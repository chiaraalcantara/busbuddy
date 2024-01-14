import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Map from './pages/Map/Map';
import BusRegistration from './pages/BusRegistration/BusRegistration';
import UserProvider from './components/Contexts/UserProvider';
import Login from './components/Login/Login';
import Home from './pages/Home/Home';

function App() {

  return (
    <UserProvider>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/map" element={<Map />} />
            <Route path="/bus-register" element={<BusRegistration />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  )
}

export default App;
