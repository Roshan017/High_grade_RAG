import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useStore } from './store';

import Header from './components/Header';
import Home from './pages/Home';
import Auth from './pages/Auth';
import Upload from './pages/Upload';
import Chat from './pages/Chat';
import Evaluation from './pages/Evaluation';

const ProtectedRoute = ({ children }) => {
  const token = useStore((state) => state.auth.token);
  if (!token) return <Navigate to="/login" replace />;
  return children;
};

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-background text-textMain font-sans">
        <Header />
        <main className="flex-1 shrink-0 flex flex-col p-4 md:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Auth mode="login" />} />
            <Route path="/signup" element={<Auth mode="signup" />} />
            <Route path="/upload" element={<ProtectedRoute><Upload /></ProtectedRoute>} />
            <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
            <Route path="/evaluation" element={<ProtectedRoute><Evaluation /></ProtectedRoute>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
