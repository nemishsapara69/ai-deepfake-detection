import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { Upload, Image as ImageIcon, AlertCircle, Loader2 } from 'lucide-react'
import axios from 'axios'

const ImageUploader = ({ setResult, setLoading, loading, setError, error }) => {
  const [preview, setPreview] = useState(null)

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    
    if (!file) return

    // Show preview
    const reader = new FileReader()
    reader.onload = () => {
      setPreview(reader.result)
    }
    reader.readAsDataURL(file)

    // Upload and get prediction
    await uploadImage(file)
  }, [])

  const uploadImage = async (file) => {
    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://localhost:5000/api/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (response.data.success) {
        setResult(response.data)
      } else {
        setError('Failed to process image')
      }
    } catch (err) {
      console.error('Upload error:', err)
      
      if (err.response?.data?.error) {
        setError(err.response.data.error)
      } else if (err.code === 'ERR_NETWORK') {
        setError('Unable to connect to the server. Make sure the backend is running on http://localhost:5000')
      } else {
        setError('An error occurred while processing the image')
      }
    } finally {
      setLoading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
    maxFiles: 1,
    maxSize: 16 * 1024 * 1024, // 16MB
    disabled: loading,
  })

  return (
    <div className="space-y-6">
      {/* Dropzone */}
      <motion.div
        {...getRootProps()}
        whileHover={{ scale: loading ? 1 : 1.02 }}
        whileTap={{ scale: loading ? 1 : 0.98 }}
        className={`
          relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
          transition-all duration-300 overflow-hidden
          ${isDragActive 
            ? 'border-blue-500 bg-blue-500/10' 
            : 'border-slate-600 hover:border-slate-500 bg-slate-800/30'
          }
          ${loading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {/* Background gradient effect */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 pointer-events-none" />
        
        <div className="relative z-10">
          {loading ? (
            <div className="flex flex-col items-center gap-4">
              <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
              <p className="text-xl font-semibold text-white">Processing Image...</p>
              <p className="text-sm text-gray-400">
                Detecting face and analyzing for deepfake patterns
              </p>
            </div>
          ) : (
            <>
              {preview ? (
                <div className="flex flex-col items-center gap-4">
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-w-xs max-h-64 rounded-lg shadow-2xl"
                  />
                  <p className="text-sm text-gray-300">
                    Image loaded. Processing...
                  </p>
                </div>
              ) : (
                <>
                  <div className="flex justify-center mb-4">
                    {isDragActive ? (
                      <Upload className="w-16 h-16 text-blue-500 animate-bounce" />
                    ) : (
                      <ImageIcon className="w-16 h-16 text-gray-400" />
                    )}
                  </div>
                  
                  <h3 className="text-2xl font-semibold text-white mb-2">
                    {isDragActive ? 'Drop image here' : 'Upload Image'}
                  </h3>
                  
                  <p className="text-gray-400 mb-4">
                    Drag & drop an image or click to browse
                  </p>
                  
                  <div className="flex justify-center gap-2 text-sm text-gray-500">
                    <span className="px-3 py-1 bg-slate-700 rounded-full">JPG</span>
                    <span className="px-3 py-1 bg-slate-700 rounded-full">JPEG</span>
                    <span className="px-3 py-1 bg-slate-700 rounded-full">PNG</span>
                  </div>
                  
                  <p className="text-xs text-gray-500 mt-4">
                    Maximum file size: 16MB
                  </p>
                </>
              )}
            </>
          )}
        </div>
      </motion.div>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 flex items-start gap-3"
        >
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-red-500 font-semibold">Error</p>
            <p className="text-red-400 text-sm mt-1">{error}</p>
          </div>
        </motion.div>
      )}

      {/* Instructions */}
      <div className="bg-slate-800/30 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <h4 className="text-white font-semibold mb-3">📋 Instructions</h4>
        <ul className="space-y-2 text-sm text-gray-400">
          <li className="flex items-start gap-2">
            <span className="text-blue-500 font-bold">1.</span>
            Upload a clear image containing a face (JPG, JPEG, or PNG format)
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-500 font-bold">2.</span>
            Our AI will detect the face and analyze it for deepfake patterns
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-500 font-bold">3.</span>
            Get instant results showing if the face is real or AI-generated
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-500 font-bold">4.</span>
            View confidence scores and the detected face region
          </li>
        </ul>
      </div>
    </div>
  )
}

export default ImageUploader
