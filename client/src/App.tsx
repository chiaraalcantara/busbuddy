import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import Login from './components/Login/Login';
import './App.css';
import UserProvider from './components/Contexts/UserProvider';


function App() {

  return (
    <UserProvider>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            {/* <Route path="/" element={<Home />} /> */}
            {/* <Route path="/map" element={<Map />} /> */}
            {/* <Route path="/register" element={<Register />} /> */}
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  )
}

export default App;
