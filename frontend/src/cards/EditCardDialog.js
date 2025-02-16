import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const EditCardDialog = ({ open, onClose, onSubmit, card }) => {
  const navigate = useNavigate();
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (card) {
      setQuestion(card.question);
      setAnswer(card.answer);
    }
  }, [card]);

  const handleSubmit = async () => {
    try {
      if (!question.trim()) {
        setError('Card question is required');
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/auth/login');
        return;
      }

      await onSubmit({
        id: card.id,
        question: question.trim(),
        answer: answer.trim()
      });
      
      setError('');
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to update card');
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Edit Card</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Question"
          fullWidth
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          error={!!error}
          helperText={error}
        />
        <TextField
          margin="dense"
          label="Answer"
          fullWidth
          multiline
          rows={4}
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditCardDialog;