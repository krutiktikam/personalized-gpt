import { useState } from 'react';
import { LoginPage } from './pages/LoginPage';
import { Dashboard } from './pages/Dashboard';
import { AnimatePresence } from 'framer-motion';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('aura_token'));

  const handleLoginSuccess = (newToken: string) => {
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('aura_token');
    setToken(null);
  };

  return (
    <div className="w-full min-h-screen bg-cyber-black text-white selection:bg-neon-cyan/30">
      <AnimatePresence mode="wait">
        {!token ? (
          <LoginPage key="login" onLoginSuccess={handleLoginSuccess} />
        ) : (
          <Dashboard key="dashboard" onLogout={handleLogout} />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
