import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ListTodo, Plus, CheckCircle2, Circle, Clock, Briefcase } from 'lucide-react';
import api from '../services/api';

interface Task {
  name: string;
  project: string;
  status: string;
  due: string | null;
}

export const TaskExplorer: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [newTask, setNewTask] = useState({ name: '', project: 'Portfolio' });

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await api.get('/tasks');
      setTasks(response.data);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.name.trim()) return;

    try {
      await api.post('/tasks', {
        task_name: newTask.name,
        project_name: newTask.project
      });
      setNewTask({ name: '', project: 'Portfolio' });
      setIsAdding(false);
      fetchTasks();
    } catch (err) {
      console.error('Failed to add task:', err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="flex flex-col h-full space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <ListTodo className="w-6 h-6 text-neon-cyan" />
          Strategic Task Planner
        </h2>
        <button 
          onClick={() => setIsAdding(!isAdding)}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-neon-cyan text-cyber-black font-bold text-sm hover:shadow-[0_0_15px_rgba(0,243,255,0.4)] transition-all"
        >
          <Plus className="w-4 h-4" />
          {isAdding ? 'CANCEL' : 'NEW TASK'}
        </button>
      </div>

      {isAdding && (
        <motion.form 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          onSubmit={addTask}
          className="p-6 rounded-2xl bg-white/5 border border-neon-cyan/30 backdrop-blur-md flex flex-col md:flex-row gap-4"
        >
          <input 
            type="text"
            placeholder="What needs to be done?"
            value={newTask.name}
            onChange={(e) => setNewTask({...newTask, name: e.target.value})}
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-neon-cyan/50"
            required
          />
          <input 
            type="text"
            placeholder="Project (e.g. Portfolio)"
            value={newTask.project}
            onChange={(e) => setNewTask({...newTask, project: e.target.value})}
            className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white focus:outline-none focus:border-neon-cyan/50 md:w-48"
          />
          <button type="submit" className="bg-neon-cyan text-cyber-black px-6 py-2 rounded-xl font-bold uppercase text-xs">
            Add to Grid
          </button>
        </motion.form>
      )}

      <div className="flex-1 bg-white/5 rounded-3xl border border-white/10 p-8 overflow-y-auto backdrop-blur-sm">
        {loading ? (
          <div className="h-full flex flex-col items-center justify-center opacity-20">
            <Clock className="w-12 h-12 animate-pulse mb-4" />
            <p className="font-mono uppercase tracking-widest text-sm">Accessing Task Grid...</p>
          </div>
        ) : tasks.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mb-6 border border-white/10">
              <ListTodo className="w-10 h-10 text-white/10" />
            </div>
            <h3 className="text-lg font-semibold text-white/40">Task Grid Empty</h3>
            <p className="text-white/20 text-sm max-w-xs mt-2">
              No active objectives found. Use the "New Task" button or ask Aura to help you plan.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {tasks.map((task, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.05 }}
                className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 hover:border-white/20 transition-all group"
              >
                <div className="cursor-pointer">
                  {task.status === 'completed' ? (
                    <CheckCircle2 className="w-6 h-6 text-neon-cyan" />
                  ) : (
                    <Circle className="w-6 h-6 text-white/20 group-hover:text-neon-cyan/50 transition-colors" />
                  )}
                </div>
                
                <div className="flex-1">
                  <h4 className={`text-sm font-medium ${task.status === 'completed' ? 'text-white/40 line-through' : 'text-white'}`}>
                    {task.name}
                  </h4>
                  <div className="flex gap-4 mt-1">
                    <div className="flex items-center gap-1.5 text-[10px] text-white/30 font-mono uppercase">
                      <Briefcase className="w-3 h-3" />
                      {task.project}
                    </div>
                    {task.due && (
                      <div className="flex items-center gap-1.5 text-[10px] text-neon-magenta/50 font-mono uppercase">
                        <Clock className="w-3 h-3" />
                        {new Date(task.due).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                </div>

                <div className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[8px] font-mono text-white/40 uppercase tracking-widest">
                  {task.status}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      <div className="p-6 rounded-2xl bg-neon-magenta/5 border border-neon-magenta/10">
        <p className="text-xs text-white/40 leading-relaxed">
          <strong className="text-neon-magenta/80 uppercase">AI Synchronization:</strong> Aura uses your task grid to provide relevant advice. 
          Ask "What should I work on today?" to get a personalized recommendation based on your skills and deadlines.
        </p>
      </div>
    </div>
  );
};
