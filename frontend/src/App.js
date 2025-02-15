import React from 'react';
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignupPage from './pages/SignupPage';
import Dashboard from './pages/Dashboard';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './auth/ProtectedRoute';

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/auth/login" element={<LoginPage />} />
                    <Route path="/auth/signup" element={<SignupPage />} />
                    <Route 
                        path="/folders" 
                        element={
                            <ProtectedRoute>
                                <Dashboard />
                            </ProtectedRoute>
                        } 
                    />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;
