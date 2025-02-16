import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { Box, Button, Card, CardContent, IconButton, List, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../utils/api';
import CreateCardDialog from './CreateCardDialog';

const CardList = () => {
  const { folderId } = useParams();
  const navigate = useNavigate();
  const [cards, setCards] = useState([]);
  const [folder, setFolder] = useState(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [error, setError] = useState('');
  const [visibleAnswers, setVisibleAnswers] = useState({});

  useEffect(() => {
    if (!folderId) {
      navigate('/folders');
      return;
    }
    loadFolder();
    loadCards();
  }, [folderId, navigate]);

  const loadFolder = async () => {
    try {
      const response = await api.folders.getById(folderId);
      if (!response.ok) {
        throw new Error('Failed to load folder');
      }
      const data = await response.json();
      setFolder(data);
    } catch (err) {
      setError('Failed to load folder');
      console.error('Error loading folder:', err);
    }
  };

  const loadCards = async () => {
    try {
      const response = await api.cards.getByFolderId(folderId);
      if (!response.ok) {
        throw new Error('Failed to load cards');
      }
      const data = await response.json();
      setCards(data);
    } catch (err) {
      setError('Failed to load cards');
      console.error('Error loading cards:', err);
    }
  };

  const handleCreateCard = async (cardData) => {
    try {
      const response = await api.cards.create({
        folder_name: folder.name,
        ...cardData
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create card');
      }
      
      setIsCreateDialogOpen(false);
      loadCards();
    } catch (err) {
      setError(err.message || 'Failed to create card');
      console.error('Error creating card:', err);
    }
  };

  const handleDeleteCard = async (cardId) => {
    try {
      const response = await api.cards.delete(cardId);
      if (!response.ok) {
        throw new Error('Failed to delete card');
      }
      setCards(cards.filter(card => card.id !== cardId));
    } catch (err) {
      setError('Failed to delete card');
      console.error('Error deleting card:', err);
    }
  };

  const toggleAnswer = (cardId) => {
    setVisibleAnswers(prev => ({
      ...prev,
      [cardId]: !prev[cardId]
    }));
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 4, p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">{folder?.name}</Typography>
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => setIsCreateDialogOpen(true)}
        >
          Add Card
        </Button>
      </Box>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <List>
        {cards.map((card) => (
          <Card key={card.id} sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="h6" gutterBottom>
                    Question:
                  </Typography>
                  <Typography sx={{ mb: 2 }}>
                    {card.question}
                  </Typography>
                  <Typography variant="h6" gutterBottom>
                    Answer:
                  </Typography>
                  {visibleAnswers[card.id] ? (
                    <Typography>
                      {card.answer}
                    </Typography>
                  ) : (
                    <Button
                      startIcon={<VisibilityIcon />}
                      onClick={() => toggleAnswer(card.id)}
                      variant="outlined"
                      size="small"
                    >
                      Show Answer
                    </Button>
                  )}
                </Box>
                <Box>
                  {visibleAnswers[card.id] && (
                    <IconButton
                      onClick={() => toggleAnswer(card.id)}
                      sx={{ mr: 1 }}
                    >
                      <VisibilityOffIcon />
                    </IconButton>
                  )}
                  <IconButton 
                    onClick={() => handleDeleteCard(card.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </Box>
            </CardContent>
          </Card>
        ))}
      </List>

      <CreateCardDialog
        open={isCreateDialogOpen}
        onClose={() => setIsCreateDialogOpen(false)}
        onSubmit={handleCreateCard}
      />
    </Box>
  );
};

export default CardList;