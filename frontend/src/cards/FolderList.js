import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { Box, Button, IconButton, List, ListItem, ListItemSecondaryAction, ListItemText, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CreateFolderDialog from '../cards/CreateFolderDialog';
import api from '../utils/api';
import EditFolderDialog from './EditFolderDialog';

const FolderList = () => {
  const [folders, setFolders] = useState([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [error, setError] = useState('');
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadFolders();
  }, []);

  const loadFolders = async () => {
    try {
      const response = await api.folders.getAll();
      if (!response.ok) {
        throw new Error('Failed to load folders');
      }
      const data = await response.json();
      setFolders(data);
    } catch (err) {
      setError('Failed to load folders');
    }
  };

  const handleCreateFolder = async (name) => {
    loadFolders(); // Refresh the list after creation
  };

  const handleDeleteFolder = async (folder) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await fetch('http://127.0.0.1:5000/folders/delete_folder', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ folder_name: folder.name })
      });

      if (response.status === 401) {
        navigate('/login');
        return;
      }

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to delete folder');
      }

      // Remove the deleted folder from the state
      setFolders(folders.filter(f => f.id !== folder.id));
    } catch (error) {
      console.error('Error deleting folder:', error);
      // Add error handling UI feedback here if needed
    }
  };

  const handleFolderClick = (folderId) => {
    navigate(`/folders/${folderId}`);
  };

  const handleEditClick = (event, folder) => {
    event.stopPropagation(); // Prevent folder click event
    setSelectedFolder(folder);
    setIsEditDialogOpen(true);
  };

  const handleEditSubmit = async (updatedFolder) => {
    try {
      setFolders(folders.map(folder => 
        folder.id === updatedFolder.id ? updatedFolder : folder
      ));
    } catch (error) {
      console.error('Error updating folder:', error);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4, p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">My Folders</Typography>
        <Button 
          variant="contained" 
          onClick={() => setIsDialogOpen(true)}
        >
          New Folder
        </Button>
      </Box>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <List>
        {folders.map((folder) => (
          <ListItem 
            key={folder.id} 
            divider 
            onClick={() => handleFolderClick(folder.id)}
            sx={{ cursor: 'pointer' }}
          >
            <ListItemText primary={folder.name} />
            <ListItemSecondaryAction>
              <IconButton 
                edge="end" 
                onClick={(e) => handleEditClick(e, folder)}
                sx={{ mr: 1 }}
              >
                <EditIcon />
              </IconButton>
              <IconButton 
                edge="end" 
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteFolder(folder);
                }}
              >
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>

      <CreateFolderDialog
        open={isDialogOpen}
        onClose={() => setIsDialogOpen(false)}
        onSubmit={handleCreateFolder}
      />

      <EditFolderDialog
        open={isEditDialogOpen}
        onClose={() => {
          setIsEditDialogOpen(false);
          setSelectedFolder(null);
        }}
        onSubmit={handleEditSubmit}
        folder={selectedFolder}
      />
    </Box>
  );
};

export default FolderList;