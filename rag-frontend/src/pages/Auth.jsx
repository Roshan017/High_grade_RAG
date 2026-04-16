import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useStore } from "../store";
import { Shield } from "lucide-react";
import axios from "axios";

import api from "../api";

export default function Auth({ mode = "login" }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const setAuth = useStore((state) => state.setAuth);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (mode === "signup") {
        await api.post("/auth/signup", { name, email, password });
        alert("Signup successful! Please login.");
        navigate("/login");
        return;
      }

      const res = await api.post("/auth/login", { email, password });
      const { access_token, user } = res.data;

      setAuth(access_token, user);
      navigate("/upload");
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col lg:flex-row min-h-full w-full">
      {/* Left Form Side */}
      <div className="flex-1 flex flex-col items-center justify-center p-4 md:p-8">
        <div className="w-full max-w-sm space-y-6 md:space-y-8">
          <div className="flex flex-col items-center pb-6 md:pb-8 border-b border-border/50">
            <Shield className="w-8 h-8 text-primary mb-4" />
            <h2 className="text-2xl md:text-3xl font-light text-textMain tracking-wide text-center">
              Establish{" "}
              <span className="text-primary italic font-semibold">
                Sovereignty
              </span>
            </h2>
            <p className="text-xs md:text-sm text-textMuted mt-3 text-center">
              Join the intelligence frontier. Secure your digital monolith.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="space-y-4 md:space-y-6 bg-surface p-6 md:p-8 rounded-2xl border border-border shadow-2xl"
          >
            <div className="space-y-4">
              <div>
                <label className="block text-[10px] font-semibold tracking-widest text-textMuted uppercase mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="sentinel@truthguard.ai"
                  className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors text-textMain placeholder:text-gray-700 font-mono"
                />
              </div>
              <div>
                <label className="block text-[10px] font-semibold tracking-widest text-textMuted uppercase mb-2">
                  Security Phrase
                </label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••••"
                  className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors text-textMain placeholder:text-gray-600 font-mono tracking-widest"
                />
              </div>
              {mode === "signup" && (
                <div>
                  <label className="block text-[10px] font-semibold tracking-widest text-textMuted uppercase mb-2">
                    Display Name
                  </label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Sentinel"
                    className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors text-textMain placeholder:text-gray-600 font-mono"
                  />
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary hover:bg-blue-600 text-white font-medium py-3.5 rounded-lg transition-all flex items-center justify-center shadow-[0_4px_14px_0_rgba(59,130,246,0.39)] hover:shadow-[0_6px_20px_rgba(59,130,246,0.23)] disabled:opacity-50"
            >
              {loading
                ? "Processing..."
                : mode === "login"
                  ? "Login"
                  : "Sign Up"}
            </button>

            <div className="text-center text-xs text-textMuted pt-4 border-t border-border/50">
              {mode === "login" ? (
                <span>
                  Don't have an account?{" "}
                  <Link
                    to="/signup"
                    className="text-textMain hover:text-primary transition-colors"
                  >
                    Sign Up
                  </Link>
                </span>
              ) : (
                <span>
                  Already have an account?{" "}
                  <Link
                    to="/login"
                    className="text-textMain hover:text-primary transition-colors"
                  >
                    Login
                  </Link>
                </span>
              )}
            </div>
          </form>

          <div className="flex items-center justify-between text-[10px] tracking-widest text-textMuted uppercase px-4 font-mono">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              Sentinel Online
            </div>
            <div className="flex gap-4">
              <Link to="#" className="hover:text-textMain">
                Legal
              </Link>
              <Link to="#" className="hover:text-textMain">
                Privacy
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Right Graphic Side */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-surface to-background border-l border-border relative overflow-hidden items-center justify-center">
        {/* Placeholder for the obelisk graphic */}
        <div
          className="absolute inset-0 opacity-20 pointer-events-none"
          style={{
            backgroundImage:
              "radial-gradient(circle at center, #3B82F6 0%, transparent 60%)",
          }}
        />
        <div className="w-48 xl:w-64 h-full bg-surface border-x border-border/50 transform rotate-12 scale-150 flex items-center justify-center shadow-2xl relative z-10">
          <Shield className="w-24 xl:w-32 h-24 xl:h-32 text-border transform -rotate-12" />
        </div>
      </div>
    </div>
  );
}
