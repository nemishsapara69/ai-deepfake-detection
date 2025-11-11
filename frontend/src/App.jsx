import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ImageUploader from './components/ImageUploader'
import ResultDisplay from './components/ResultDisplay'
import Header from './components/Header'
import Footer from './components/Footer'

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Video Background */}
      <div className="fixed inset-0 z-0">
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute w-full h-full object-cover opacity-20"
        >
          <source src="/background.mp4" type="video/mp4" />
        </video>
        {/* Overlay for better readability */}
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/80 via-slate-900/70 to-slate-900/80"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        <Header />
        
        <main className="flex-grow container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-4xl mx-auto"
        >
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold mb-4 gradient-text">
              Deepfake Detection
            </h1>
            <p className="text-xl text-gray-300">
              Upload an image to verify if it contains a real or AI-generated face
            </p>
            <div className="mt-4 flex justify-center gap-4 text-sm text-gray-400">
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                Powered by EfficientNet
              </span>
              <span className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                MTCNN Face Detection
              </span>
            </div>
          </div>

          {/* Main Content */}
          <AnimatePresence mode="wait">
            {!result ? (
              <motion.div
                key="uploader"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3 }}
              >
                <ImageUploader
                  setResult={setResult}
                  setLoading={setLoading}
                  loading={loading}
                  setError={setError}
                  error={error}
                />
              </motion.div>
            ) : (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.3 }}
              >
                <ResultDisplay result={result} onReset={handleReset} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Info Cards */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="text-lg font-semibold text-white mb-2">High Accuracy</h3>
              <p className="text-gray-400 text-sm">
                Our model is trained on thousands of real and fake faces for reliable detection
              </p>
            </div>
            
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="text-lg font-semibold text-white mb-2">Fast Processing</h3>
              <p className="text-gray-400 text-sm">
                Get results in seconds with our optimized deep learning pipeline
              </p>
            </div>
            
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
              <div className="text-3xl mb-3">🔒</div>
              <h3 className="text-lg font-semibold text-white mb-2">Privacy First</h3>
              <p className="text-gray-400 text-sm">
                Your images are processed securely and not stored on our servers
              </p>
            </div>
          </motion.div>
        </motion.div>
      </main>

      <Footer />
      </div>
    </div>
  )
}

export default App
