import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Zap, Cpu, HardDrive, ShieldCheck } from 'lucide-react';
import api from '../services/api';

export const StatsDashboard: React.FC = () => {
  const [stats, setStats] = useState({
    latency: '0ms',
    uptime_seconds: 0,
    core_load: '0%',
    persistence: 'Checking...'
  });

  const fetchStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const formatUptime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    const hours = Math.floor(mins / 60);
    const displayMins = mins % 60;
    
    if (hours > 0) return `${hours}h ${displayMins}m`;
    return `${mins}m ${secs}s`;
  };

  const statCards = [
    { label: 'Neural Latency', value: stats.latency, icon: Zap, color: 'text-neon-cyan' },
    { label: 'System Uptime', value: formatUptime(stats.uptime_seconds), icon: Activity, color: 'text-neon-magenta' },
    { label: 'Core Load', value: stats.core_load, icon: Cpu, color: 'text-white' },
    { label: 'Neural Persistence', value: stats.persistence, icon: HardDrive, color: 'text-neon-cyan' },
  ];

  return (
    <div className="flex flex-col h-full space-y-8">
      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, idx) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="p-6 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm"
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-2xl bg-white/5 border border-white/5 ${stat.color}`}>
                <stat.icon className="w-5 h-5" />
              </div>
              <div className="px-2 py-0.5 rounded bg-white/5 border border-white/5 text-[8px] font-mono text-white/20 uppercase tracking-widest">
                Real-time
              </div>
            </div>
            <h3 className="text-white/40 text-xs uppercase tracking-widest font-mono mb-1">{stat.label}</h3>
            <p className="text-2xl font-bold text-white tracking-tight">{stat.value}</p>
          </motion.div>
        ))}
      </div>

      {/* Main Stats Visualization */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white/5 rounded-3xl border border-white/10 p-8 flex flex-col relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-neon-cyan/40 to-transparent" />
          
          <div className="flex justify-between items-center mb-10">
            <div>
              <h3 className="text-lg font-bold">Neural Connectivity Stream</h3>
              <p className="text-white/20 text-xs font-mono">ENCRYPTED TUNNEL: AURA_SECURE_v4</p>
            </div>
            <ShieldCheck className="w-6 h-6 text-neon-cyan/40" />
          </div>

          <div className="flex-1 flex items-end gap-2 px-2">
            {[...Array(30)].map((_, i) => {
              const height = Math.random() * 60 + 20;
              return (
                <motion.div
                  key={i}
                  animate={{ height: `${height}%` }}
                  transition={{ duration: 1.5, repeat: Infinity, repeatType: 'reverse', delay: i * 0.05 }}
                  className="flex-1 bg-neon-cyan/20 rounded-t-sm border-t border-neon-cyan/40"
                />
              );
            })}
          </div>
        </div>

        <div className="bg-white/5 rounded-3xl border border-white/10 p-8 flex flex-col items-center justify-center text-center">
          <div className="relative mb-8">
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
              className="w-40 h-40 rounded-full border border-dashed border-neon-cyan/20"
            />
            <div className="absolute inset-0 flex flex-col items-center justify-center">
               <span className="text-3xl font-bold text-neon-cyan">99.9<span className="text-sm">%</span></span>
               <span className="text-[10px] text-white/20 font-mono uppercase tracking-widest">Accuracy</span>
            </div>
          </div>
          <h4 className="text-sm font-semibold mb-2 uppercase tracking-widest">Model Integrity</h4>
          <p className="text-white/40 text-xs leading-relaxed max-w-[180px]">
            Neural parameters are currently within optimal thresholds for high-precision inference.
          </p>
        </div>
      </div>
    </div>
  );
};
