import { create } from 'zustand';

export const useStore = create((set) => ({
  auth: {
    token: localStorage.getItem("token") || null,
    user: null
  },
  document: {
    id: null,
    filename: null,
    status: null, // 'processed', etc.
    preview: null,
    fileUrl: null
  },
  chat: {
    messages: [],
    queryCount: 0
  },
  evaluation: {
    faithfulness: null,
    answer_relevancy: null
  },

  setAuth: (token, user) => {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
    set({ auth: { token, user } });
  },

  setDocument: (doc) => set({ document: doc }),

  appendMessage: (msg) => set((state) => {
    const isUser = msg.role === 'user';
    return {
      chat: {
        ...state.chat,
        messages: [...state.chat.messages, msg],
        queryCount: isUser ? state.chat.queryCount + 1 : state.chat.queryCount
      }
    };
  }),

  setEvaluation: (evalData) => set({ evaluation: evalData }),

  resetStore: () => {
    localStorage.removeItem("token");
    set({
      auth: { token: null, user: null },
      document: { id: null, filename: null, status: null },
      chat: { messages: [], queryCount: 0 },
      evaluation: { faithfulness: null, answer_relevancy: null }
    });
  }
}));
