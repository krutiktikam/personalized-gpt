import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageSquare, 
  BrainCircuit, 
  Activity, 
  LogOut, 
  Settings,
  ChevronRight,
  ListTodo,
  Menu,
  X
} from 'lucide-react';
import { AuraAvatar } from '../components/AuraAvatar';
import { ChatWindow } from '../components/ChatWindow';
import { MemoryExplorer } from '../components/MemoryExplorer';
import { StatsDashboard } from '../components/StatsDashboard';
import { TaskExplorer } from '../components/TaskExplorer';

interface DashboardProps {
  onLogout: () => void;
}

type Tab = 'chat' | 'memory' | 'stats' | 'tasks';

export const Dashboard: React.FC<DashboardProps> = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState<Tab>('chat');
  const [auraEmotion, setAuraEmotion] = useState('neutral');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Close sidebar when clicking a link on mobile
  const handleTabChange = (tab: Tab) => {
    setActiveTab(tab);
    if (window.innerWidth < 1024) {
      setIsSidebarOpen(false);
    }
  };

  const getEmotionColor = () => {
    switch (auraEmotion) {
      case 'happy': return 'from-neon-green/20';
      case 'sad': return 'from-blue-500/20';
      case 'angry': return 'from-neon-red/20';
      case 'architect': return 'from-neon-magenta/20';
      case 'review': return 'from-neon-orange/20';
      default: return 'from-neon-cyan/10';
    }
  };

  return (
    <div className="flex h-screen w-full bg-cyber-black overflow-hidden text-white font-sans relative">
      {/* Background Dynamic Glow */}
      <div className={`fixed inset-0 bg-gradient-to-br ${getEmotionColor()} to-transparent transition-colors duration-1000 pointer-events-none z-0`} />
      
      {/* Mobile Backdrop */}
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsSidebarOpen(false)}
            className="fixed inset-0 bg-cyber-black/80 backdrop-blur-sm z-30 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <aside className={`
        fixed inset-y-0 left-0 w-72 bg-white/5 border-r border-white/10 flex flex-col p-6 z-40 backdrop-blur-xl transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between mb-12">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-neon-cyan flex items-center justify-center">
              <div className="w-4 h-4 border-2 border-cyber-black rounded-sm" />
            </div>
            <h2 className="text-xl font-bold tracking-tight">AURA CORE</h2>
          </div>
          <button 
            onClick={() => setIsSidebarOpen(false)}
            className="p-2 hover:bg-white/5 rounded-lg lg:hidden"
          >
            <X className="w-5 h-5 text-white/60" />
          </button>
        </div>

        <nav className="flex-1 space-y-2">
          {sidebarItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleTabChange(item.id as Tab)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${
                  isActive 
                    ? 'bg-neon-cyan text-cyber-black font-semibold shadow-[0_0_15px_rgba(0,243,255,0.3)]' 
                    : 'hover:bg-white/5 text-white/60 hover:text-white'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-cyber-black' : 'text-white/40 group-hover:text-neon-cyan'}`} />
                <span>{item.label}</span>
                {isActive && <ChevronRight className="ml-auto w-4 h-4" />}
              </button>
            );
          })}
        </nav>

        <div className="pt-6 border-t border-white/10 space-y-2">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-white/40 hover:text-white hover:bg-white/5 transition-all">
            <Settings className="w-5 h-5" />
            <span>Settings</span>
          </button>
          <button 
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-red-400/60 hover:text-red-400 hover:bg-red-400/10 transition-all"
          >
            <LogOut className="w-5 h-5" />
            <span>Terminate</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 relative flex flex-col overflow-hidden w-full">
        {/* Background Aura Visualization */}
        <div className="absolute top-0 right-0 p-6 lg:p-12 z-0 opacity-30 lg:opacity-50 pointer-events-none">
          <AuraAvatar emotion={auraEmotion} />
        </div>

        {/* Tab Header */}
        <header className="px-6 lg:px-10 py-6 lg:py-8 border-b border-white/5 bg-cyber-black/50 backdrop-blur-md z-20 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 hover:bg-white/5 rounded-lg lg:hidden"
            >
              <Menu className="w-6 h-6 text-neon-cyan" />
            </button>
            <div>
              <h1 className="text-lg lg:text-3xl font-bold uppercase tracking-widest text-white/90 line-clamp-1">
                {activeTab === 'chat' && 'Live Chat Terminal'}
                {activeTab === 'tasks' && 'Strategic Task Grid'}
                {activeTab === 'memory' && 'Neural Memory Explorer'}
                {activeTab === 'stats' && 'Internal System Health'}
              </h1>
              <p className="text-neon-cyan/60 text-[10px] lg:text-xs mt-0.5 lg:mt-1 font-mono uppercase">
                STATUS: STABLE // CONNECTION: ENCRYPTED
              </p>
            </div>
          </div>
          
          <div className="hidden sm:flex gap-4">
            <div className="px-3 py-1 rounded-full bg-neon-cyan/10 border border-neon-cyan/30 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-neon-cyan animate-pulse" />
              <span className="text-[10px] text-neon-cyan font-bold">API ONLINE</span>
            </div>
          </div>
        </header>

        {/* Tab Content */}
        <div className="flex-1 overflow-auto p-4 lg:p-10 z-10 relative">
          <AnimatePresence mode="wait">
            {activeTab === 'chat' && (
              <motion.div
                key="chat"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="h-full"
              >
                <ChatWindow onEmotionChange={setAuraEmotion} />
              </motion.div>
            )}

            {activeTab === 'tasks' && (
              <motion.div
                key="tasks"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="h-full"
              >
                <TaskExplorer />
              </motion.div>
            )}

            {activeTab === 'memory' && (
              <motion.div
                key="memory"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="h-full"
              >
                <MemoryExplorer />
              </motion.div>
            )}

            {activeTab === 'stats' && (
              <motion.div
                key="stats"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="h-full"
              >
                <StatsDashboard />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
