import { useAuth } from '../context/AuthContext';

function HomePage() {
  const { user, logout } = useAuth();

  return (
    <div>
      <h1>Welcome {user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default HomePage;