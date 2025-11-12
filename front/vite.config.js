import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['heic2any']
  },
  server: {
    fs: {
      allow: ['..']
    }
  }
})
