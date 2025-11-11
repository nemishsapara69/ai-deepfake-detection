import { motion } from 'framer-motion'
import { CheckCircle, XCircle, RotateCcw, AlertTriangle, Users } from 'lucide-react'

const ResultDisplay = ({ result, onReset }) => {
  const { prediction, face_detection, face_crop } = result

  const isFake = prediction.result === 'Fake'
  const confidence = prediction.confidence

  return (
    <div className="space-y-6">
      {/* Main Result Card */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', duration: 0.5 }}
        className={`
          relative overflow-hidden rounded-2xl p-8 border-2
          ${isFake 
            ? 'bg-red-500/10 border-red-500/50' 
            : 'bg-green-500/10 border-green-500/50'
          }
        `}
      >
        {/* Background glow effect */}
        <div className={`
          absolute inset-0 blur-3xl opacity-20
          ${isFake ? 'bg-red-500' : 'bg-green-500'}
        `} />

        <div className="relative z-10">
          {/* Result Icon and Label */}
          <div className="flex items-center justify-center mb-6">
            {isFake ? (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1, rotate: [0, -10, 10, -10, 0] }}
                transition={{ delay: 0.2, duration: 0.5 }}
              >
                <XCircle className="w-24 h-24 text-red-500" strokeWidth={1.5} />
              </motion.div>
            ) : (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              >
                <CheckCircle className="w-24 h-24 text-green-500" strokeWidth={1.5} />
              </motion.div>
            )}
          </div>

          <h2 className={`
            text-4xl font-bold text-center mb-2
            ${isFake ? 'text-red-400' : 'text-green-400'}
          `}>
            {isFake ? '🔴 Fake Detected' : '🟢 Real Image'}
          </h2>

          <p className="text-center text-gray-300 text-lg">
            {isFake 
              ? 'This image appears to be AI-generated or manipulated'
              : 'This image appears to contain a genuine face'
            }
          </p>

          {/* Confidence Score */}
          <div className="mt-8">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-400">Confidence</span>
              <span className="text-2xl font-bold text-white">{confidence.toFixed(1)}%</span>
            </div>
            
            {/* Progress Bar */}
            <div className="relative h-6 bg-slate-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${confidence}%` }}
                transition={{ delay: 0.3, duration: 0.8, ease: 'easeOut' }}
                className={`
                  h-full rounded-full
                  ${isFake 
                    ? 'bg-gradient-to-r from-red-600 to-red-500' 
                    : 'bg-gradient-to-r from-green-600 to-green-500'
                  }
                `}
              />
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-xs font-bold text-white mix-blend-difference">
                  {confidence.toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          {/* Probability Breakdown */}
          <div className="mt-6 grid grid-cols-2 gap-4">
            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span className="text-sm text-gray-400">Fake Probability</span>
              </div>
              <p className="text-2xl font-bold text-red-400">
                {prediction.fake_probability.toFixed(1)}%
              </p>
            </div>

            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-400">Real Probability</span>
              </div>
              <p className="text-2xl font-bold text-green-400">
                {prediction.real_probability.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Face Detection Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Detected Face */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700"
        >
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-blue-500" />
            Detected Face
          </h3>
          
          {face_crop && (
            <img
              src={face_crop}
              alt="Detected face"
              className="w-full rounded-lg shadow-lg mb-4"
            />
          )}
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Detection Confidence</span>
              <span className="text-white font-semibold">
                {(face_detection.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Faces Detected</span>
              <span className="text-white font-semibold">
                {face_detection.num_faces}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Face Region</span>
              <span className="text-white font-semibold text-xs">
                {face_detection.box[2]} × {face_detection.box[3]}px
              </span>
            </div>
          </div>
        </motion.div>

        {/* Analysis Details */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700"
        >
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-yellow-500" />
            Analysis Details
          </h3>
          
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-400 mb-2">Model Score</p>
              <div className="bg-slate-700 rounded-lg p-3">
                <code className="text-xs text-green-400">
                  Raw Score: {prediction.raw_score.toFixed(6)}
                </code>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-400 mb-2">Interpretation</p>
              <div className="text-sm text-gray-300 space-y-1">
                <p>• Scores closer to 0 indicate synthetic/fake content</p>
                <p>• Scores closer to 1 indicate authentic/real content</p>
                <p>• Model uses deep learning patterns to detect artifacts</p>
              </div>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
              <p className="text-xs text-blue-300">
                ℹ️ This analysis is based on AI detection and should be used as a reference tool.
                Always verify critical information through multiple sources.
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Reset Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="flex justify-center"
      >
        <button
          onClick={onReset}
          className="
            flex items-center gap-2 px-8 py-4 
            bg-gradient-to-r from-blue-600 to-purple-600 
            hover:from-blue-700 hover:to-purple-700
            text-white font-semibold rounded-xl
            transition-all duration-300 transform hover:scale-105
            shadow-lg hover:shadow-xl
          "
        >
          <RotateCcw className="w-5 h-5" />
          Analyze Another Image
        </button>
      </motion.div>
    </div>
  )
}

export default ResultDisplay
