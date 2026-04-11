import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BrainCircuit, Trash2, RefreshCcw, Tag } from 'lucide-react';
import api from '../services/api';

interface MemoryItem {
  category: string;
  value: string;
  timestamp?: string;
}

export const MemoryExplorer: React.FC = () => {
  const [memory, setMemory] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchMemory = async () => {
    setLoading(true);
    try {
      const response = await api.get('/memory');
      setMemory(response.data);
    } catch (err) {
      console.error('Failed to fetch memory:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearMemory = async () => {
    if (!confirm("Are you sure you want to wipe Aura's neural memory? This cannot be undone.")) return;
    try {
      await api.delete('/memory/clear');
      setMemory([]);
    } catch (err) {
      console.error('Failed to clear memory:', err);
    }
  };

  useEffect(() => {
    fetchMemory();
  }, []);

  return (
    <div className="flex flex-col h-full space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <BrainCircuit className="w-6 h-6 text-neon-cyan" />
          Extracted User Knowledge
        </h2>
        <div className="flex gap-3">
          <button 
            onClick={fetchMemory}
            className="p-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 text-white/60 hover:text-white transition-all"
            title="Refresh Memory"
          >
            <RefreshCcw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button 
            onClick={clearMemory}
            className="p-2 rounded-lg bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 text-red-400 transition-all"
            title="Clear All Memory"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="flex-1 bg-white/5 rounded-3xl border border-white/10 p-8 overflow-y-auto backdrop-blur-sm">
        {loading ? (
          <div className="h-full flex flex-col items-center justify-center opacity-20">
            <RefreshCcw className="w-12 h-12 animate-spin mb-4" />
            <p className="font-mono uppercase tracking-widest text-sm">Syncing Neural Grid...</p>
          </div>
        ) : memory.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mb-6 border border-white/10">
              <BrainCircuit className="w-10 h-10 text-white/10" />
            </div>
            <h3 className="text-lg font-semibold text-white/40">No Knowledge Detected</h3>
            <p className="text-white/20 text-sm max-w-xs mt-2">
              Aura hasn't extracted any specific facts yet. Try sharing your hobbies or skills in the chat.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {memory.map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.05 }}
                className="p-4 rounded-2xl bg-white/5 border border-white/5 hover:border-neon-cyan/30 hover:bg-white/10 transition-all group"
              >
                <div className="flex items-center gap-2 mb-2">
                  <Tag className="w-3 h-3 text-neon-cyan/50" />
                  <span className="text-[10px] font-mono uppercase tracking-widest text-neon-cyan/60">{item.category}</span>
                </div>
                <p className="text-white/90 font-medium">{item.value}</p>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      <div className="p-6 rounded-2xl bg-neon-cyan/5 border border-neon-cyan/10">
        <p className="text-xs text-white/40 leading-relaxed">
          <strong className="text-neon-cyan/80 uppercase">Pro Tip:</strong> Neural extraction is autonomous. 
          When you mention a skill (e.g., "I know React") or a preference, Aura automatically stores it to personalize future interactions.
        </p>
      </div>
    </div>
  );
};
