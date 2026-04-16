import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '../store';
import { Upload as UploadIcon, FileText, CheckCircle2, Shield, Zap, Eye, BarChart2 } from 'lucide-react';
import api from '../api';

export default function Upload() {
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  
  const navigate = useNavigate();
  const setDocument = useStore((state) => state.setDocument);
  const currentDoc = useStore((state) => state.document);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = async (file) => {
    setLoading(true);
    try {
      const formData = new FormData(); 
      formData.append("file", file);
      
      const res = await api.post('/doc-upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      // Extract preview snippet from backend response
      // Structure: res.data.data.fixed_size_chunks[0].text
      const graphResult = res.data.data;
      const chunks = graphResult?.fixed_size_chunks || [];
      const fullPreview = chunks.slice(0, 5).map(c => c.text).join("\n\n");
      const snippet = fullPreview || "Preview not available.";

      // Generate Blob URL for full-document iframe preview
      if (currentDoc.fileUrl) {
        URL.revokeObjectURL(currentDoc.fileUrl);
      }
      const fileUrl = URL.createObjectURL(file);

      setDocument({
        id: "doc_" + Date.now(),
        filename: file.name,
        status: "processed",
        size: (file.size / 1024 / 1024).toFixed(1) + " MB",
        preview: snippet,
        fileUrl: fileUrl,
        data: res.data
      });
    } catch (err) {
      console.error(err);
      alert('Failed to upload document.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 w-full max-w-6xl mx-auto py-4 md:py-8">
      
      <div className="mb-8 md:mb-12">
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-textMain mb-4">
          Ingest <span className="text-primary bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-400">Intelligence.</span>
        </h1>
        <p className="text-base md:text-lg text-textMuted max-w-xl">
          Secure document analysis for the TruthGuard ecosystem. Deploy local AI models to verify integrity and extract metadata.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Left Col - Upload Area & Features */}
        <div className="space-y-6">
          <div 
            className={`flex flex-col items-center justify-center p-6 md:p-12 border-2 border-dashed rounded-2xl transition-all duration-300 ${dragActive ? 'border-primary bg-primary/5 scale-[1.02]' : 'border-border bg-surface hover:border-gray-600 hover:bg-surface/80'}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="w-12 h-12 md:w-16 md:h-16 rounded-2xl bg-gray-800 border border-border flex items-center justify-center mb-6 text-primary">
               {loading ? <UploadIcon className="w-6 h-6 md:w-8 md:h-8 animate-bounce" /> : <UploadIcon className="w-6 h-6 md:w-8 md:h-8" />}
            </div>
            
            <h3 className="text-xl md:text-2xl font-semibold text-textMain mb-2">Upload Document</h3>
            <p className="text-textMuted mb-8 text-center text-xs md:text-sm">Drag and drop files here or click to browse</p>
            
            <div className="flex flex-wrap justify-center gap-2 md:gap-3 mb-8">
              <span className="px-3 py-1 rounded-md bg-background border border-border text-[10px] md:text-xs font-mono font-medium text-textMuted">PDF</span>
              <span className="px-3 py-1 rounded-md bg-background border border-border text-[10px] md:text-xs font-mono font-medium text-textMuted">DOCX</span>
              <span className="px-3 py-1 rounded-md bg-background border border-border text-[10px] md:text-xs font-mono font-medium text-textMuted">TXT</span>
            </div>

            <input 
              ref={fileInputRef}
              type="file" 
              className="hidden" 
              accept=".pdf,.docx,.txt"
              onChange={handleChange}
            />
            
            <button 
              onClick={() => fileInputRef.current.click()}
              disabled={loading}
              className="w-full sm:w-auto px-6 py-3 bg-primary/20 text-primary hover:bg-primary/30 font-medium rounded-lg transition-colors border border-primary/20 hover:border-primary/40 disabled:opacity-50"
            >
              {loading ? 'Processing Neural Data...' : 'Select Files'}
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 md:gap-6">
            <div className="bg-surface border border-border p-4 md:p-6 rounded-2xl">
              <Shield className="w-5 h-5 md:w-6 md:h-6 text-primary mb-4" />
              <h4 className="font-semibold text-textMain mb-2 text-sm md:text-base">Sovereign Encryption</h4>
              <p className="text-[10px] md:text-xs text-textMuted leading-relaxed">Files are encrypted using AES-256 before ingestion. Your data remains your own.</p>
            </div>
            <div className="bg-surface border border-border p-4 md:p-6 rounded-2xl">
              <Zap className="w-5 h-5 md:w-6 md:h-6 text-emerald-400 mb-4" />
              <h4 className="font-semibold text-textMain mb-2 text-sm md:text-base">Neural Parsing</h4>
              <p className="text-[10px] md:text-xs text-textMuted leading-relaxed">Automatic OCR and semantic indexing are applied during the upload sequence.</p>
            </div>
          </div>
        </div>

        {/* Right Col - Activity */}
        <div className="space-y-6 lg:pl-8 lg:border-l border-border/50">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold text-textMain flex items-center gap-2">
              Recent Activity
              <span className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
            </h3>
            <button className="text-xs font-semibold tracking-wider text-textMuted uppercase hover:text-primary transition-colors">View All</button>
          </div>

          {currentDoc.filename ? (
            <div className="bg-surface border border-border rounded-xl p-1 shadow-lg shadow-black/20 group relative overflow-hidden">
               <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/10 to-transparent pointer-events-none" />
               <div className="absolute left-0 top-0 bottom-0 w-1 bg-emerald-500" />
               <div className="p-5 flex flex-col gap-4">
                 
                 <div className="flex items-start justify-between relative z-10">
                   <div className="flex items-center gap-4">
                     <div className="w-10 h-10 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400 border border-emerald-500/20">
                       <FileText className="w-5 h-5" />
                     </div>
                     <div>
                       <h4 className="font-medium text-textMain">{currentDoc.filename}</h4>
                       <p className="text-xs text-textMuted">{currentDoc.size || '1.2 MB'} • {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</p>
                     </div>
                   </div>
                   <span className="px-2 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded text-[10px] font-mono font-semibold uppercase tracking-wider">
                     {currentDoc.status}
                   </span>
                 </div>

                 <div className="bg-background/50 border border-border rounded-lg p-4 font-mono text-xs italic text-textMuted">
                   {currentDoc.preview || "No preview available for this document."}
                 </div>

                 <div className="flex items-center gap-4 pt-2 relative z-10">
                    <button 
                      onClick={() => alert(`Document Preview:\n\n${currentDoc.preview || 'No preview available.'}`)}
                      className="flex items-center gap-2 text-xs font-medium text-textMuted hover:text-textMain transition-colors"
                    >
                      <Eye className="w-4 h-4" /> Preview
                    </button>
                    <button 
                      onClick={() => navigate('/chat')}
                      className="flex items-center gap-2 text-xs font-medium text-primary hover:text-blue-400 transition-colors ml-auto"
                    >
                      <BarChart2 className="w-4 h-4" /> Analyze in Chat &rarr;
                    </button>
                 </div>

               </div>
            </div>
          ) : (
             <div className="flex flex-col items-center justify-center h-48 border border-border border-dashed rounded-xl bg-surface/50">
                <FileText className="w-8 h-8 text-border mb-3" />
                <p className="text-textMuted text-sm">No recent documents</p>
             </div>
          )}

        </div>
      </div>
    </div>
  );
}
