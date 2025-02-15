import { Box, Button, CircularProgress, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login(formData.email, formData.password);
      setFormData({ email: '', password: '' });
      navigate("/folders");
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 400, mx: 'auto', mt: 4 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>Login</Typography>
      
      {error && (
        <Typography 
          color="error" 
          sx={{ mb: 2, p: 1, bgcolor: 'error.light', borderRadius: 1 }}
        >
          {error}
        </Typography>
      )}
      
      <TextField
        fullWidth
        label="Email"
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        margin="normal"
        required
        disabled={isLoading}
        error={!!error}
      />
      <TextField
        fullWidth
        label="Password"
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        margin="normal"
        required
        disabled={isLoading}
        error={!!error}
      />
      <Button
        type="submit"
        variant="contained"
        fullWidth
        disabled={isLoading}
        sx={{ mt: 2 }}
      >
        {isLoading ? <CircularProgress size={24} /> : 'Login'}
      </Button>
    </Box>
  );
};

export default LoginForm;