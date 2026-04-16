import { useState, useEffect } from 'react';
import { useStore } from '../store';
import { FileText, AlertTriangle, Rocket, CheckCircle, Search, ZoomIn, ZoomOut } from 'lucide-react';
import api from '../api';

export default function Evaluation() {
  const { faithfulness, answer_relevancy } = useStore((state) => state.evaluation);
  const setEvaluation = useStore((state) => state.setEvaluation);
  const { messages, queryCount } = useStore((state) => state.chat);
  const currentDoc = useStore((state) => state.document);
  const [loading, setLoading] = useState(false);
  
  const userQueries = messages.filter(m => m.role === 'user');

  const runEvaluation = async () => {
    setLoading(true);
    try {
      const res = await api.post('/analyze');
      const { faithfulness, answer_relevancy } = res.data;
      setEvaluation({ faithfulness, answer_relevancy });
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.message || 'Failed to run RAGAS evaluation.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 w-full max-w-7xl mx-auto h-auto min-h-full py-4 px-2 md:px-0">
      
      <div className="mb-6 flex flex-col sm:flex-row shrink-0 justify-between items-start sm:items-end gap-3 md:gap-0">
        <div>
           <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-textMain mb-1">RAGAS Evaluation</h1>
           <p className="text-textMuted text-base md:text-lg">Evaluate answer quality and grounding</p>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 flex-1 min-h-0">
        
        {/* Left Col - Document Viewer */}
        <div className="flex-[2] min-h-[400px] md:min-h-[500px] lg:min-h-0 bg-surface border border-border rounded-xl flex flex-col overflow-hidden shadow-xl">
          <div className="bg-background px-3 md:px-4 py-3 border-b border-border flex justify-between items-center shrink-0">
             <div className="flex items-center gap-2 text-sm font-medium text-textMain">
                <FileText className="w-4 h-4 text-primary" />
                {currentDoc.filename || "No_Document_Selected.pdf"}
             </div>
             <div className="flex items-center gap-4 text-xs text-textMuted">
                <span className="bg-surface px-2 py-1 rounded">Page 1 of 24</span>
                <button className="hover:text-textMain"><ZoomOut className="w-3.5 h-3.5" /></button>
                <button className="hover:text-textMain"><ZoomIn className="w-3.5 h-3.5" /></button>
             </div>
          </div>
          
          <div className="flex-1 bg-surface relative overflow-hidden">
            {currentDoc.fileUrl && !currentDoc.filename?.endsWith('.docx') ? (
              <iframe 
                src={currentDoc.fileUrl} 
                className="w-full h-full border-none"
                title="Document Preview"
              />
            ) : (
              <div className="p-8 h-full overflow-y-auto custom-scrollbar bg-[#1a1f2e] text-gray-300 relative">
                 <h2 className="text-xl font-bold text-white mb-6 uppercase tracking-wider border-b border-gray-700 pb-4">
                    {currentDoc.filename || "Document Analysis"}
                 </h2>
                 
                 {currentDoc.filename?.endsWith('.docx') && (
                   <div className="mb-6 p-4 bg-amber-500/10 border border-amber-500/20 rounded-lg text-amber-500 text-xs flex items-center gap-2">
                     <AlertTriangle className="w-4 h-4" />
                     Native .DOCX preview is not supported by your browser. Showing extracted text summary below.
                   </div>
                 )}

                 <div className="space-y-6 text-sm leading-relaxed font-light">
                    {currentDoc.preview ? currentDoc.preview.split('\n\n').map((p, i) => (
                      <p key={i}>{p}</p>
                    )) : (
                      <div className="flex flex-col items-center justify-center py-20 opacity-30">
                        <FileText className="w-12 h-12 mb-4" />
                        <p>No document content available for evaluation preview.</p>
                      </div>
                    )}
                 </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Col - Controls & Metrics */}
        <div className="flex-1 flex flex-col gap-6 overflow-y-auto lg:custom-scrollbar">
          
          <div className="bg-surface border border-border rounded-xl flex flex-col">
            <div className="px-5 py-4 border-b border-border bg-background/50">
               <h3 className="text-[10px] font-bold tracking-widest uppercase text-textMuted">Recent Queries</h3>
            </div>
            <div className="flex-1 p-3 flex flex-col gap-2 relative min-h-[200px] overflow-y-auto custom-scrollbar">
              {userQueries.length === 0 ? (
                <div className="absolute inset-0 flex flex-col items-center justify-center text-textMuted opacity-50">
                   <Search className="w-8 h-8 mb-2" />
                   <p className="text-xs">No queries yet</p>
                </div>
              ) : (
                userQueries.map((q, i) => (
                  <div key={i} className="p-3 border border-border bg-background/50 rounded-lg hover:border-gray-600 transition-colors">
                    <h4 className="text-sm font-medium text-textMain mb-1 line-clamp-1">{q.content}</h4>
                    <p className="text-xs text-textMuted line-clamp-1">Correlating port delays with fiscal underperformance...</p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-surface border border-border rounded-xl p-5 shadow-lg relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent pointer-events-none" />
            
            {queryCount < 10 && (
              <div className="mb-4 flex items-start gap-3 p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-amber-500">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                <p className="text-xs leading-relaxed">
                  For accurate evaluation, more than 10 queries are recommended. Currently: {queryCount}/10
                </p>
              </div>
            )}

            <button 
              onClick={runEvaluation}
              disabled={queryCount < 5 || loading}
              className={`w-full py-4 rounded-lg flex items-center justify-center gap-2 font-bold tracking-wider uppercase transition-all duration-300 relative z-10 ${queryCount >= 5 ? 'bg-teal-500 hover:bg-teal-400 text-teal-950 shadow-[0_4px_20px_rgba(20,184,166,0.3)]' : 'bg-surface border border-border text-textMuted cursor-not-allowed opacity-50'}`}
            >
              {loading ? <div className="w-5 h-5 border-2 border-teal-950 border-t-transparent rounded-full animate-spin" /> : <Rocket className="w-5 h-5" />}
              {loading ? 'Evaluating...' : 'Run Evaluation'}
            </button>
          </div>

          <div className="bg-surface border border-border rounded-xl p-6 relative overflow-hidden mt-auto shrink-0 shadow-2xl">
             <div className="flex items-center justify-between mb-8">
               <h3 className="text-xs font-bold tracking-widest uppercase text-teal-400">Ragas Metric Output</h3>
               <div className="w-8 h-8 rounded-full bg-border flex items-center justify-center">
                  <CheckCircle className="w-4 h-4 text-textMuted" />
               </div>
             </div>

             <div className="space-y-6">
               <MetricBar label="Faithfulness" value={faithfulness} color="bg-emerald-400" />
               <MetricBar label="Answer Relevancy" value={answer_relevancy} color="bg-cyan-400" />
             </div>

             <div className="mt-8 flex items-center justify-between border-t border-border/50 pt-4 text-[10px] tracking-widest uppercase font-mono text-textMuted">
                 <div className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
                    Intelligence Active
                 </div>
                 <span>v2.4.0-prod</span>
             </div>
          </div>

        </div>

      </div>
    </div>
  );
}

function MetricBar({ label, value, color }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-textMain">{label}</span>
        <span className="text-lg font-bold text-textMain">{value ? value.toFixed(2) : '--'}</span>
      </div>
      <div className="h-2 w-full bg-background rounded-full overflow-hidden border border-border relative">
        <div 
          className={`absolute top-0 bottom-0 left-0 ${color} rounded-full transition-all duration-1000 ease-out`} 
          style={{ width: value ? `${value * 100}%` : '0%' }}
        />
      </div>
    </div>
  );
}
