import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [
      vue(),
      tailwindcss(),
    ],
    server: {
      host: '0.0.0.0',
      port: 3000,

      allowedHosts: [
        env.VITE_PUBLIC_HOST,
      ],

      hmr: {
        protocol: 'wss',     // 🔥 ОБЯЗАТЕЛЬНО
        host: env.VITE_PUBLIC_HOST,
        clientPort: 443,
      },
    },
  }
})
