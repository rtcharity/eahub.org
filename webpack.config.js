const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  context: __dirname,
  entry: './eahub/base/static/scripts/main',
  output: {
      path: path.resolve('./eahub/base/static/webpack_bundles/'),
      filename: "[name]-[hash].js",
  },
  devtool: '#eval-source-map',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.css$/i,
        use: [
          {
            // Adds CSS to the DOM by injecting a `<style>` tag
            loader: 'style-loader'
          },
          {
            // Interprets `@import` and `url()` like `import/require()` and will resolve them
            loader: 'css-loader'
          }
        ]
      },
      {
        test: /\.less$/,
        loader: 'less-loader', // compiles Less to CSS
      },
      {
          test: /\.(woff(2)?|ttf|eot|png|jpe?g|gif)(\?v=\d+\.\d+\.\d+)?$/,
          use: [{
              loader: 'file-loader',
              options: {
                  name: '[name].[ext]',
                  outputPath: 'fonts/'
              }
          }]
      },
      {
        test: /\.svg$/,
        loader: 'svg-inline-loader'
      },
      {
        test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
        use: {
          loader: "url-loader",
          options: {
            // Limit at 50k. Above that it emits separate files
            limit: 50000,

            // url-loader sets mimetype if it's passed.
            // Without this it derives it from the file extension
            mimetype: "application/font-woff",

            // Output below fonts directory
            name: "./fonts/[name].[ext]",
          }
        }
      },
    ]
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.HotModuleReplacementPlugin(),
    new CleanWebpackPlugin(),
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery'
    }),
  ],
}
