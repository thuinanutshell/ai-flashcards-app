import { Box, Button, Container, Typography } from '@mui/material';
import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();

    return (
        <Container maxWidth="sm">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 3
                }}
            >
                <Typography component="h1" variant="h3">
                    AI Flashcards App
                </Typography>
                
                <Typography variant="h6" color="text.secondary" align="center">
                    Create and study flashcards with AI assistance
                </Typography>

                <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
                    <Button
                        variant="contained"
                        color="primary"
                        size="large"
                        onClick={() => navigate('/auth/login')}
                    >
                        Log In
                    </Button>
                    <Button
                        variant="outlined"
                        color="primary"
                        size="large"
                        onClick={() => navigate('/auth/signup')}
                    >
                        Sign Up
                    </Button>
                </Box>
            </Box>
        </Container>
    );
};

export default HomePage;
