import * as esbuild from 'esbuild'
import {sassPlugin} from 'esbuild-sass-plugin'

/* handle dev vs production settings */
const env = "development";
const is_prod = (env==="production");

await esbuild.build({
    entryPoints: ["app/entrypoint.js"],
    outdir: "build",
    publicPath: "/static/react",
    assetNames: "[name]-[hash].digested",
    bundle: true,
    minify: is_prod,
    sourcemap: !is_prod,
    watch: (process.argv.includes("--watch")),
    target: "es6",
    loader: {".js": "jsx",
	     ".png": "file"},
    plugins: [sassPlugin()]
})
    .then(() => console.log("esbuild is running."))
    .catch(() => process.exit(1))


