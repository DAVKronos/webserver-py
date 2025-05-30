import * as esbuild from 'esbuild'
import {sassPlugin} from 'esbuild-sass-plugin'

const is_prod = process.env.NODE_ENV === 'production';


await esbuild.build({
    entryPoints: ["app/entrypoint.js"],
    outdir: "build",
    publicPath: "/static/react",
    assetNames: "[name]-[hash].digested",
    bundle: true,
    minify: is_prod,
    sourcemap: !is_prod,
    define: {
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
    },
    watch: (process.argv.includes("--watch")),
    target: "es6",
    loader: {".js": "jsx",
	     ".png": "file"},
    plugins: [sassPlugin()]
})
    .then(() => console.log("esbuild is running."))
    .catch(() => process.exit(1))


