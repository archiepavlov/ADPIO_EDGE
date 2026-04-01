import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],

  //Custom to ADPIO_EDGE WEB-INF
  build: {
    outDir: '../ADPIO_EDGE/WEB-INF',
    rollupOptions: {
      treeshake: true,
      output: {
        entryFileNames: 'assets/index.js',
        chunkFileNames: 'assets/index-chunk.js',
        assetFileNames: 'assets/[name].[ext]',
      },
    },
  }

})
