import { Container } from '@mui/material';
import React from 'react';
import SignupForm from '../auth/SignupForm';

const SignupPage = () => {
  return (
    <Container maxWidth="sm">
      <SignupForm />
    </Container>
  );
};

export default SignupPage;
