const API_BASE_URL = 'http://127.0.0.1:5000';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
    'Accept': 'application/json'
  };
};

const defaultOptions = {
  mode: 'cors',
  credentials: 'include',
  headers: getHeaders()
};

const api = {
  auth: {
    signup: (data) => fetch(`${API_BASE_URL}/auth/signup`, {
      ...defaultOptions,
      method: 'POST',
      body: JSON.stringify(data)
    }),
    login: async (email, password) => {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        ...defaultOptions,
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Login failed');
      }

      return response.json();
    },
    logout: () => fetch(`${API_BASE_URL}/auth/logout`, {
      ...defaultOptions,
      method: 'POST'
    }),
    checkStatus: () => fetch(`${API_BASE_URL}/auth/status`, {
      ...defaultOptions,
      headers: getHeaders()
    })
  },
  folders: {
    getAll: () => fetch(`${API_BASE_URL}/folders/`, {
      ...defaultOptions,
      headers: getHeaders()
    }),
    create: (data) => fetch(`${API_BASE_URL}/folders/create_folder`, {
      ...defaultOptions,
      headers: getHeaders(),
      method: 'POST',
      body: JSON.stringify(data)
    }),
    delete: (id) => fetch(`${API_BASE_URL}/folders/delete_folder/${id}`, {
      ...defaultOptions,
      method: 'DELETE'
    }),
    getById: (id) => 
      fetch(`${API_BASE_URL}/folders/${id}`, {
        ...defaultOptions,
        method: 'GET',
        headers: getHeaders()
      })
  },
  cards: {
    getAll: (folderName) => fetch(`${API_BASE_URL}/cards/get_cards${folderName ? `?folder_name=${folderName}` : ''}`, {
      ...defaultOptions,
      headers: getHeaders()
    }),
    create: (data) => fetch(`${API_BASE_URL}/cards/create_card`, {
      ...defaultOptions,
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        folder_name: data.folder_name,
        question: data.question,
        answer: data.answer
      })
    }),
    update: async (cardId, data) => {
      const response = await fetch(`${API_BASE_URL}/cards/update_card`, {
        ...defaultOptions,
        method: 'PUT',
        headers: getHeaders(),
        body: JSON.stringify({
          card_id: cardId,
          question: data.question,
          answer: data.answer
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update card');
      }
      
      return response;
    },
    delete: (cardId) => fetch(`${API_BASE_URL}/cards/delete_card`, {
      ...defaultOptions,
      method: 'DELETE',
      headers: getHeaders(),
      body: JSON.stringify({ card_id: cardId })
    }),
    getByFolderId: (folderId) => 
      fetch(`${API_BASE_URL}/cards/get_cards?folder_id=${folderId}`, {
        ...defaultOptions,
        method: 'GET',
        headers: getHeaders()
      })
  }
};

export default api;
