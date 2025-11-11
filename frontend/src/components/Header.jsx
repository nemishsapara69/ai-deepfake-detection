import { motion } from 'framer-motion'
import { Shield, Github } from 'lucide-react'

const Header = () => {
  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-slate-800/50 backdrop-blur-md border-b border-slate-700 sticky top-0 z-50"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Deepfake Detector</h1>
              <p className="text-xs text-gray-400">AI-Powered Face Verification</p>
            </div>
          </div>
          
          <nav className="flex items-center gap-4">
            <a
              href="#"
              className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg transition-colors text-sm"
            >
              <Github className="w-4 h-4" />
              GitHub
            </a>
          </nav>
        </div>
      </div>
    </motion.header>
  )
}

export default Header
