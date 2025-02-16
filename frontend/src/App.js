import React from 'react';
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import ProtectedRoute from './auth/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import CardListPage from './pages/CardListPage';
import Dashboard from './pages/Dashboard';
import LoginPage from "./pages/LoginPage";
import SignupPage from './pages/SignupPage';

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
                    <Route 
                        path="/folders/:folderId/cards" 
                        element={
                            <ProtectedRoute>
                                <CardListPage />
                            </ProtectedRoute>
                        } 
                    />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;
