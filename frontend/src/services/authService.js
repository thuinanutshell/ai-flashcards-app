const API_URL = 'http://127.0.0.1:5000'; // this tells you the link of the backend which remains constant

export const authService = {
  signup: async (userData) => {
    const response = await fetch(`${API_URL}/auth/signup`, { // this fetches the data from the backend
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  },

  login: async (credentials) => {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    return data;
  }
}; // if you have more features, just add more link connected to the backend (for example, logout)