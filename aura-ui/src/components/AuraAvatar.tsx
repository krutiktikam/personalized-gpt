import { motion, AnimatePresence } from 'framer-motion';

interface AuraAvatarProps {
  emotion: string;
}

const emotionStyles: Record<string, { color: string; scale: number; speed: number }> = {
  happy: { color: 'rgba(57, 255, 20, 0.8)', scale: 1.1, speed: 2 },
  sad: { color: 'rgba(59, 130, 246, 0.6)', scale: 0.9, speed: 4 },
  angry: { color: 'rgba(255, 49, 49, 0.8)', scale: 1.2, speed: 1 },
  neutral: { color: 'rgba(0, 243, 255, 0.4)', scale: 1.0, speed: 3 },
  architect: { color: 'rgba(255, 0, 255, 0.8)', scale: 1.2, speed: 1.5 },
  review: { color: 'rgba(255, 94, 0, 0.8)', scale: 1.05, speed: 1.2 },
};

export const AuraAvatar = ({ emotion }: AuraAvatarProps) => {
  const style = emotionStyles[emotion] || emotionStyles.neutral;

  return (
    <div className="relative w-48 h-48 flex items-center justify-center">
      {/* Outer Glow */}
      <motion.div
        animate={{
          scale: [style.scale, style.scale * 1.2, style.scale],
          opacity: [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: style.speed,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="absolute inset-0 rounded-full blur-3xl"
        style={{ backgroundColor: style.color }}
      />
      
      {/* Core Orb */}
      <motion.div
        animate={{
          scale: [1, 1.05, 1],
          boxShadow: [
            `0 0 20px ${style.color}`,
            `0 0 60px ${style.color}`,
            `0 0 20px ${style.color}`
          ]
        }}
        transition={{
          duration: style.speed,
          repeat: Infinity,
          ease: "linear"
        }}
        className="w-24 h-24 rounded-full bg-white relative z-10"
        style={{ 
          background: `radial-gradient(circle at 30% 30%, white, ${style.color})` 
        }}
      />

      {/* Internal Particle/Swirl (Optional expansion point) */}
      <div className="absolute inset-0 z-20 overflow-hidden rounded-full pointer-events-none">
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="w-full h-full border-t-2 border-white/20 rounded-full"
        />
      </div>
    </div>
  );
};
