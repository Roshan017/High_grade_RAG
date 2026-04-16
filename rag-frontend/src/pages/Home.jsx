import { Link } from 'react-router-dom';
import { UploadCloud, MessageSquare, CheckCircle, Shield } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 w-full max-w-6xl mx-auto py-8 md:py-12">
      
      {/* Hero Section */}
      <div className="text-center space-y-4 md:space-y-6 mb-12 md:mb-20">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface border border-border text-[10px] md:text-xs font-semibold text-emerald-400 mb-2 md:mb-4 tracking-wider">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
          SENTINEL ENGINE ACTIVE
        </div>
        <h1 className="text-4xl sm:text-6xl md:text-8xl font-bold tracking-tight text-textMain">
          TruthGuard <span className="text-primary bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-400">AI</span>
        </h1>
        <p className="text-lg md:text-xl text-textMuted max-w-2xl mx-auto font-light">
          Verify documents using AI-powered retrieval and reasoning. Establish an authoritative source of truth for your most critical data.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6">
          <Link to="/signup" className="w-full sm:w-auto text-center px-8 py-3.5 bg-primary hover:bg-blue-600 text-white font-medium rounded-xl transition-all shadow-[0_0_20px_rgba(59,130,246,0.3)] hover:shadow-[0_0_30px_rgba(59,130,246,0.5)]">
            Sign Up &rarr;
          </Link>
          <Link to="/login" className="w-full sm:w-auto text-center px-8 py-3.5 bg-surface hover:bg-gray-800 text-textMain font-medium rounded-xl border border-border transition-all">
            Login
          </Link>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
        <FeatureCard 
          icon={<UploadCloud className="w-6 h-6 text-primary" />}
          title="Upload documents"
          desc="Securely ingest PDF, Word, and text documents into our encrypted vault. Support for multi-lingual and scanned content."
        />
        <FeatureCard 
          icon={<MessageSquare className="w-6 h-6 text-teal-400" />}
          title="Ask questions"
          desc="Interact with your knowledge base using natural language. Our reasoning engine analyzes context across your entire library."
        />
        <FeatureCard 
          icon={<CheckCircle className="w-6 h-6 text-emerald-400" />}
          title="Get grounded answers"
          desc="Receive precise answers backed by direct citations. Eliminate hallucinations through deterministic document retrieval."
        />
      </div>

    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="flex flex-col p-8 bg-surface rounded-2xl border border-border hover:border-gray-700 transition-colors group hover:-translate-y-1 duration-300">
      <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-gray-800 border border-gray-700 mb-6 group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-3 text-textMain">{title}</h3>
      <p className="text-textMuted leading-relaxed bg-surface">{desc}</p>
    </div>
  );
}
