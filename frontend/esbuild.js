import * as esbuild from 'esbuild'
import { sassPlugin } from 'esbuild-sass-plugin'

const isProd = process.env.NODE_ENV === 'production'
const watch = process.argv.includes('--watch')

const options = {
  entryPoints: ['app/entrypoint.js'],
  outdir: 'build',
  publicPath: '/static/react',
  assetNames: '[name]-[hash].digested',
  bundle: true,
  minify: isProd,
  sourcemap: !isProd,
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
  },
  target: 'es2020',
  loader: { '.js': 'jsx', '.png': 'file' },
  plugins: [sassPlugin({
    // Bootstrap 4's SCSS triggers a wall of Dart Sass deprecation warnings; they go away with Bootstrap 5.
    quietDeps: true,
    silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'abs-percent', 'if-function']
  })]
}

try {
  if (watch) {
    const ctx = await esbuild.context(options)
    await ctx.watch()
    console.log('esbuild is watching for changes...')
  } else {
    await esbuild.build(options)
    console.log('esbuild build finished.')
  }
} catch {
  process.exit(1)
}
