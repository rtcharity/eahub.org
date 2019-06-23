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
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|jpe?g|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {},
          },
        ],
      },
    ]
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.HotModuleReplacementPlugin(),
    new CleanWebpackPlugin(),
  ],
}
