import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Profile from './pages/profile';
import Chat from './pages/chat';
import SignIn from './pages/sign-in';
import SignUp from './pages/sign-up';
import SignOut from './pages/sign-out';
import KeyGen from './pages/key-gen';
import Payments from './pages/payments';
import ProtectedRoute from './components/ProtectedRoute';
import { useAuth } from './hooks/useAuth';

function App() {
  const { currentUser } = useAuth();
  console.log(currentUser?.getIdToken());

  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            {!currentUser ? (
              <>
                <li><Link to="/sign-up">Sign Up</Link></li>
                <li><Link to="/sign-in">Sign In</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/sign-out">Sign Out</Link></li>
                <li><Link to="/key-gen">Key Gen</Link></li>
                <li><Link to="/payments">Payments</Link></li>
              </>
            )}
            
            <li><Link to="/chat">Chat</Link></li>
            <li><Link to="/profile">Profile</Link></li>
          </ul>
        </nav>

        <Routes>
          <Route path="/profile" element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          } />
          <Route path="/chat" element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          } />
          <Route path="/key-gen" element={
            <ProtectedRoute>
              <KeyGen />
            </ProtectedRoute>
          } />
          <Route path="/payments" element={
            <ProtectedRoute>
              <Payments />
            </ProtectedRoute>
          } />
          <Route path="/sign-in" element={<SignIn />} />
          <Route path="/sign-up" element={<SignUp />} />
          <Route path="/sign-out" element={<SignOut />} />

          <Route path="/" element={<SignUp />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
