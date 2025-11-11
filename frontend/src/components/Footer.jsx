import { Heart } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="bg-slate-800/30 backdrop-blur-sm border-t border-slate-700 py-6 mt-12">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-gray-400">
            © 2025 Deepfake Detection. All rights reserved.
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-400">
            Made with <Heart className="w-4 h-4 text-red-500 fill-red-500" /> using React, TensorFlow & AI
          </div>
          
          <div className="flex gap-4 text-sm">
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Terms of Service
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              Contact
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
