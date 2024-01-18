import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CustomSidebar from './pages/global/Sidebar'; 
import Documentation from './pages/Documentation';
import LogReader from './pages/LogReader';
import Dashboard from './pages/Dashboard';
import LoadImage from './pages/LoadFunction';
import CaptureImage from './pages/CaptureFunction';
function App() {
  return (
    <Router>
      <div id="app" style={{ height: "100vh", display: "flex" }}>
        <div style={{ position: 'fixed' }}>
          <CustomSidebar />
        </div>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/load" element={<LoadImage />} />
          <Route path="/capture" element={<CaptureImage />} />
          <Route path="/log" element={<LogReader />} />
          <Route path="/documentation" element={<Documentation />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;