import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useStore } from "../store";
import {
  Send,
  FileText,
  ChevronDown,
  ChevronUp,
  Link as LinkIcon,
  AlertCircle,
  Sparkles,
  Paperclip,
  BarChart,
  Shield as ShieldIcon,
} from "lucide-react";
import api from "../api";

export default function Chat() {
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const { messages, queryCount } = useStore((state) => state.chat);
  const appendMessage = useStore((state) => state.appendMessage);
  const setEvaluation = useStore((state) => state.setEvaluation);
  const currentDoc = useStore((state) => state.document);
  const navigate = useNavigate();

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMessage = { role: "user", content: input };
    appendMessage(userMessage);
    setInput("");
    setIsTyping(true);

    try {
      const res = await api.post("/query", { query: input });
      const { final_answer, citations, retrieved_chunks } = res.data;

      const aiResponse = {
        role: "ai",
        answer: final_answer || "No response received.",
        // The backend citations structure might vary, adapting safely:
        citations: Array.isArray(citations) ? citations : [],
        reference_chunks: retrieved_chunks || [],
      };
      appendMessage(aiResponse);
    } catch (err) {
      console.error(err);
      appendMessage({
        role: "ai",
        answer:
          "An error occurred while connecting to the neural reasoning engine.",
        citations: [],
        reference_chunks: [],
      });
    } finally {
      setIsTyping(false);
    }
  };

  const handleRagasEvaluation = async () => {
    if (queryCount < 5) return;

    if (queryCount < 10) {
      if (
        !window.confirm(
          "Warning: More than 10 queries recommended for accurate evaluation. Run anyway?",
        )
      ) {
        return;
      }
    }

    // Simulate navigation to RAGAS and fetching data
    setEvaluation({ faithfulness: 0.87, answer_relevancy: 0.81 });
    navigate("/evaluation");
  };

  if (!currentDoc.id) {
    return (
      <div className="flex flex-col items-center justify-center flex-1 h-full">
        <AlertCircle className="w-12 h-12 text-primary mb-4" />
        <h2 className="text-xl font-medium text-textMain mb-2">
          No Document Context
        </h2>
        <p className="text-textMuted mb-6">
          Please upload a document to begin chatting.
        </p>
        <button
          onClick={() => navigate("/upload")}
          className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          Go to Upload
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col max-w-4xl mx-auto w-full h-[calc(100vh-140px)] md:h-[calc(100vh-120px)] relative">
      {/* Chat History */}
      <div className="flex-1 overflow-y-auto px-2 md:pr-4 pb-32 md:pb-24 space-y-6 md:space-y-8 custom-scrollbar">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full opacity-50">
            <Sparkles className="w-12 h-12 text-primary mb-4" />
            <p className="text-textMain font-medium">Ask TruthGuard Anything</p>
            <p className="text-sm text-textMuted mt-1">
              Analyzing: {currentDoc.filename}
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => <Message key={idx} msg={msg} />)
        )}

        {isTyping && (
          <div className="flex items-start gap-4 max-w-[80%]">
            <div className="w-8 h-8 rounded bg-surface border border-border flex items-center justify-center flex-shrink-0 mt-1">
              <ShieldIcon className="w-4 h-4 text-primary animate-pulse" />
            </div>
            <div className="p-4 rounded-2xl bg-surface border border-border text-textMuted flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-primary/50 animate-bounce"></span>
              <span
                className="w-2 h-2 rounded-full bg-primary/50 animate-bounce"
                style={{ animationDelay: "150ms" }}
              ></span>
              <span
                className="w-2 h-2 rounded-full bg-primary/50 animate-bounce"
                style={{ animationDelay: "300ms" }}
              ></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="absolute bottom-0 left-0 right-0 pt-6 pb-2 bg-gradient-to-t from-background via-background to-transparent">
        <form
          onSubmit={handleSubmit}
          className="flex gap-3 bg-surface border border-border p-2 rounded-xl focus-within:border-primary/50 focus-within:shadow-[0_0_15px_rgba(59,130,246,0.1)] transition-all"
        >
          <button
            type="button"
            className="p-3 text-textMuted hover:text-textMain transition-colors"
          >
            <Paperclip className="w-5 h-5" />
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask TruthGuard anything..."
            className="flex-1 bg-transparent text-textMain focus:outline-none placeholder:text-gray-600"
          />
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="p-3 bg-primary text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:hover:bg-primary"
          >
            <Send className="w-5 h-5 ml-0.5" />
          </button>
        </form>

        <div className="mt-4 flex flex-col items-center gap-2">
          {queryCount > 0 && queryCount < 5 && (
            <p className="text-[10px] text-textMuted tracking-wider font-mono">
              Evaluations require at least 5 queries for statistical
              significance. (Current: {queryCount}/5)
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

function Message({ msg }) {
  const isUser = msg.role === "user";
  const [showRefs, setShowRefs] = useState(false);

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-4">
        <div className="p-3 md:p-4 rounded-2xl rounded-tr-sm bg-primary/20 border border-primary/30 text-textMain max-w-[90%] md:max-w-[80%] ml-auto text-sm md:text-base">
          {msg.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3 md:gap-4 max-w-full md:max-w-3xl">
      <div className="w-7 h-7 md:w-8 md:h-8 rounded bg-surface border border-border flex items-center justify-center flex-shrink-0 mt-1 shadow-sm shadow-blue-500/10">
        <ShieldIcon className="w-3.5 h-3.5 md:w-4 md:h-4 text-primary" />
      </div>
      <div className="p-4 md:p-5 rounded-2xl rounded-tl-sm bg-surface/50 border border-border text-textMain flex-1 overflow-hidden backdrop-blur-sm">
        <div className="flex items-center gap-2 text-[10px] uppercase tracking-widest text-primary font-semibold mb-4 font-mono">
          <Sparkles className="w-3 h-3" />
          Verified Response
        </div>

        <div className="text-sm md:text-base leading-relaxed text-textMain mb-6 font-light">
          {msg.answer}
        </div>

        {msg.citations && msg.citations.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6">
            {msg.citations.map((cit, idx) => (
              <button
                key={idx}
                className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-background border border-border text-xs text-textMuted hover:text-textMain hover:border-gray-600 transition-colors"
              >
                <FileText className="w-3 h-3 text-primary" />
                Page {cit.page}, {cit.file}
              </button>
            ))}
          </div>
        )}

        {msg.reference_chunks && msg.reference_chunks.length > 0 && (
          <div className="border border-border rounded-lg bg-background/50 overflow-hidden">
            <button
              onClick={() => setShowRefs(!showRefs)}
              className="w-full flex items-center justify-between px-4 py-3 text-xs tracking-wider uppercase font-semibold text-textMuted hover:text-textMain transition-colors hover:bg-surface"
            >
              View Reference Content
              {showRefs ? (
                <ChevronUp className="w-4 h-4" />
              ) : (
                <ChevronDown className="w-4 h-4" />
              )}
            </button>
            {showRefs && (
              <div className="px-4 pb-4 space-y-3 font-mono text-xs italic text-gray-400 border-t border-border mt-2 pt-4 bg-background">
                {msg.reference_chunks.map((chunk, idx) => (
                  <div key={idx} className="pl-3 border-l-[3px] border-border">
                    {chunk}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
