import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite is the tool that runs and builds our React frontend.
// This config keeps setup simple and uses the React plugin.
export default defineConfig({
  plugins: [react()],
})
