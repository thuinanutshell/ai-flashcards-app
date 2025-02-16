import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import { Box, Button, Card, CardContent, IconButton, List, Typography } from '@mui/material';
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../utils/api';
import CreateCardDialog from './CreateCardDialog';
import EditCardDialog from './EditCardDialog';

const CardList = () => {
  const { folderId } = useParams();
  const navigate = useNavigate();
  const [cards, setCards] = useState([]);
  const [folder, setFolder] = useState(null);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [selectedCard, setSelectedCard] = useState(null);
  const [error, setError] = useState('');
  const [visibleAnswers, setVisibleAnswers] = useState({});

  const loadFolder = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/auth/login');
        return;
      }

      const response = await api.folders.getById(folderId);
      if (response.status === 401) {
        localStorage.removeItem('token');
        navigate('/auth/login');
        return;
      }
      
      if (!response.ok) {
        throw new Error('Failed to load folder');
      }
      
      const data = await response.json();
      setFolder(data);
    } catch (err) {
      setError('Failed to load folder');
      console.error('Error loading folder:', err);
    }
  }, [folderId, navigate]);

  const loadCards = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/auth/login');
        return;
      }

      const response = await api.cards.getByFolderId(folderId);
      if (response.status === 401) {
        localStorage.removeItem('token');
        navigate('/auth/login');
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to load cards');
      }
      
      const data = await response.json();
      setCards(data);
    } catch (err) {
      setError('Failed to load cards');
      console.error('Error loading cards:', err);
    }
  }, [folderId, navigate]);

  useEffect(() => {
    if (!folderId) {
      navigate('/folders');
      return;
    }

    loadFolder();
    loadCards();
  }, [folderId, navigate, loadFolder, loadCards]);

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

  const handleEditCard = async (updatedCard) => {
    try {
      await api.cards.update(updatedCard.id, {
        question: updatedCard.question,
        answer: updatedCard.answer
      });

      setCards(cards.map(card => 
        card.id === updatedCard.id ? updatedCard : card
      ));
      setIsEditDialogOpen(false);
      setError('');
    } catch (err) {
      setError(err.message || 'Failed to update card');
      console.error('Error updating card:', err);
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

  const openEditDialog = (card) => {
    setSelectedCard(card);
    setIsEditDialogOpen(true);
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
                    onClick={() => openEditDialog(card)}
                    sx={{ mr: 1 }}
                  >
                    <EditIcon />
                  </IconButton>
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
      
      <EditCardDialog
        open={isEditDialogOpen}
        onClose={() => setIsEditDialogOpen(false)}
        onSubmit={handleEditCard}
        card={selectedCard}
      />
    </Box>
  );
};

export default CardList;