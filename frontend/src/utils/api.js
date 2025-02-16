const API_BASE_URL = 'http://127.0.0.1:5000';

const getHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
  'Accept': 'application/json'
});

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
    })
  }
};

export default api;
