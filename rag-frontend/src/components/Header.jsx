import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useStore } from '../store';
import { LogOut, User, Settings, Shield } from 'lucide-react';

export default function Header() {
  const { token } = useStore((state) => state.auth);
  const resetStore = useStore((state) => state.resetStore);
  const location = useLocation();
  const navigate = useNavigate();

  const handleDisconnect = () => {
    if (window.confirm("Please disconnect after work to avoid unnecessary data clashes")) {
      resetStore();
      navigate("/");
    }
  };

  const navLinks = [
    { name: 'Doc Upload', path: '/upload' },
    { name: 'AI Chat', path: '/chat' },
    { name: 'RAGAS Evaluations', path: '/evaluation' }
  ];

  return (
    <header className="flex items-center justify-between px-8 py-4 border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-50">
      <Link to="/" className="flex items-center gap-2 group">
        <Shield className="w-6 h-6 text-primary group-hover:text-blue-400 transition-colors" />
        <span className="text-xl font-semibold tracking-tight text-textMain">
          TruthGuard <span className="text-primary font-bold">AI</span>
        </span>
      </Link>

      {token && (
        <nav className="flex items-center gap-8">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.name}
                to={link.path}
                className={`text-sm font-medium transition-colors hover:text-primary ${
                  isActive ? 'text-primary border-b-2 border-primary pb-1' : 'text-textMuted'
                }`}
              >
                {link.name}
              </Link>
            );
          })}
        </nav>
      )}

      <div className="flex items-center gap-4">
        {token ? (
          <>
            <button 
              onClick={handleDisconnect}
              className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-textMuted hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors border border-transparent hover:border-red-400/20"
            >
              <LogOut className="w-4 h-4" />
              <span>Disconnect</span>
            </button>
            <div className="w-px h-6 bg-border mx-2"></div>
            <button className="text-textMuted hover:text-textMain transition-colors">
              <User className="w-5 h-5" />
            </button>
            <button className="text-textMuted hover:text-textMain transition-colors">
              <Settings className="w-5 h-5" />
            </button>
          </>
        ) : (
          <div className="flex items-center gap-4">
            <Link to="/login" className="text-sm font-medium text-textMuted hover:text-textMain transition-colors">
              Login
            </Link>
            <Link to="/signup" className="text-sm font-medium px-4 py-2 bg-primary/10 text-primary hover:bg-primary/20 rounded-lg transition-colors border border-primary/20">
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}
