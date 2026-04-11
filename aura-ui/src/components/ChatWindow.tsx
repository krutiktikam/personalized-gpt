import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, User, Bot, Sparkles, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import api from '../services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWindowProps {
  onEmotionChange: (emotion: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ onEmotionChange }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('default');
  const scrollRef = useRef<HTMLDivElement>(null);

  const modes = [
    { id: 'default', label: 'Default', color: 'bg-white/10' },
    { id: 'architect', label: 'Architect', color: 'bg-neon-magenta/20 text-neon-magenta border-neon-magenta/30' },
    { id: 'review', label: 'Code Review', color: 'bg-orange-500/20 text-orange-400 border-orange-500/30' },
  ];

  const scrollToBottom = () => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: 'smooth',
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.post('/chat', {
        message: input,
        mode: mode,
      });

      const auraMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.reply,
      };

      setMessages((prev) => [...prev, auraMsg]);
      // If mode is architect/review, we force that visual style on the orb
      onEmotionChange(mode !== 'default' ? mode : response.data.emotion);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "ERROR: NEURAL LINK INTERRUPTED. Check backend connection.",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white/5 rounded-3xl border border-white/10 overflow-hidden backdrop-blur-sm">
      {/* Mode Selector */}
      <div className="px-6 py-3 border-b border-white/5 bg-white/5 flex gap-2 overflow-x-auto no-scrollbar">
        {modes.map((m) => (
          <button
            key={m.id}
            onClick={() => setMode(m.id)}
            className={`px-3 py-1 rounded-full text-[10px] uppercase tracking-widest font-bold border transition-all ${
              mode === m.id 
                ? m.color 
                : 'bg-transparent text-white/20 border-white/10 hover:border-white/20'
            }`}
          >
            {m.label}
          </button>
        ))}
      </div>

      {/* Messages area */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent"
      >
        <AnimatePresence initial={false}>
          {messages.length === 0 && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="h-full flex flex-col items-center justify-center text-center p-12"
            >
              <div className="w-16 h-16 rounded-2xl bg-neon-cyan/10 border border-neon-cyan/20 flex items-center justify-center mb-6">
                <Sparkles className="w-8 h-8 text-neon-cyan" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Initialize Neural Link</h3>
              <p className="text-white/40 max-w-xs mx-auto text-sm leading-relaxed">
                Systems are ready. Type a command or share your thoughts to begin.
              </p>
            </motion.div>
          )}

          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-4 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border ${
                  msg.role === 'user' 
                    ? 'bg-white/10 border-white/20' 
                    : 'bg-neon-cyan/10 border-neon-cyan/30'
                }`}>
                  {msg.role === 'user' ? <User className="w-4 h-4 text-white/60" /> : <Bot className="w-4 h-4 text-neon-cyan" />}
                </div>
                
                <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user' 
                    ? 'bg-white/10 text-white rounded-tr-none' 
                    : 'bg-white/5 text-white/90 border border-white/5 rounded-tl-none prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-cyber-black prose-pre:border prose-pre:border-white/10'
                }`}>
                  {msg.role === 'assistant' ? (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            </motion.div>
          ))}

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="flex gap-4 items-center">
                 <div className="w-8 h-8 rounded-lg bg-neon-cyan/10 border border-neon-cyan/30 flex items-center justify-center shrink-0">
                    <Loader2 className="w-4 h-4 text-neon-cyan animate-spin" />
                 </div>
                 <span className="text-xs font-mono text-neon-cyan/60 uppercase tracking-widest animate-pulse">Aura is thinking...</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Input area */}
      <form onSubmit={handleSend} className="p-6 bg-cyber-black/40 border-t border-white/5 backdrop-blur-md">
        <div className="relative group">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message to Aura..."
            className="w-full bg-white/5 border border-white/10 rounded-2xl pl-6 pr-14 py-4 text-white placeholder:text-white/20 focus:outline-none focus:border-neon-cyan/50 focus:ring-1 focus:ring-neon-cyan/20 transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className={`absolute right-2 top-1/2 -translate-y-1/2 p-3 rounded-xl transition-all ${
              !input.trim() || loading 
                ? 'text-white/10 cursor-not-allowed' 
                : 'text-neon-cyan hover:bg-neon-cyan/10 bg-neon-cyan/5'
            }`}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <p className="mt-3 text-[10px] text-white/10 text-center uppercase tracking-widest font-mono">
          System v2.4 // End-to-End Neural Encryption Active
        </p>
      </form>
    </div>
  );
};
