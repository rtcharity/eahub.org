const path = require('path');
const webpack = require('webpack');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require(`mini-css-extract-plugin`);
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const SentryWebpackPlugin = require("@sentry/webpack-plugin");


const config = {
  mode: 
        (process.env.NODE_ENV !== 'prod' ? 'development'  //roland
                                        : 'production'),

  context: __dirname,
  entry: {
    global_bs3: './eahub/base/static/global/main_bs3.js',
    global_bs5: './eahub/base/static/global/main_bs5.js',
    vendor_bs3: './eahub/base/static/vendor/main_bs3.js',
    vendor_bs5: './eahub/base/static/vendor/main_bs5.js',

    component_search_profiles: './eahub/base/static/components/search-profiles/main.js',
    component_similarity_search: './eahub/base/static/components/similarity-search/main.js',    //roland
    component_profile_edit: './eahub/base/static/components/profile/edit/main.js',
    component_profile_detail: './eahub/base/static/components/profile/profile-detail.js',
    component_maps: './eahub/base/static/components/maps/main.js',
    component_group_page_actions: './eahub/base/static/components/group-page-actions.js',
    component_tables: './eahub/base/static/components/tables.js',
    component_local_groups_edit: './eahub/base/static/components/local-groups-edit.js',
    component_feedback: './eahub/base/static/components/feedback.js',
  },
  output: {
    filename: '[name].js',
    path: path.resolve('./eahub/base/static/dist'),
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.svg$/i,
        loader: 'svg-url-loader',
      },
      {
        test: /\.(sass|scss|css)$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              sourceMap: true,
              plugins: () => {
                return [
                  require('precss'),
                  require('autoprefixer'),
                ];
              },
              hmr: true,
            }
          },
          {loader: 'css-loader', options: {sourceMap: true}},
          {loader: 'sass-loader', options: {sourceMap: true}},
        ]
      },
      {
        test: /\.(ttf|eot)(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
          }
        }]
      },
      {
        // images
        test: /\.(jpe?g|png|gif)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              query: {
                hash: 'sha512',
                digest: 'hex',
                name: '[name].[ext]',
              }
            }
          },
          {
            loader: 'image-webpack-loader',
            options: {
              query: {
                bypassOnDebug: 'true',
                mozjpeg: {progressive: true},
                gifsicle: {interlaced: true},
                optipng: {optimizationLevel: 7},
              }
            }
          }
        ]
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
          }
        }
      },
      {
        test: /\.vue$/,
        use: [{loader: 'vue-loader'}]
      },
    ]
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js',],
    modules: [
      path.resolve('eahub/base/static'),
      path.resolve('.'),
      'node_modules'
    ],
    alias: {
      vue: process.env.NODE_ENV === 'prod' ? 'vue/dist/vue.min.js' : 'vue/dist/vue.js',
    },
  },
  devServer: {
    contentBase: path.resolve(__dirname, `eahub/base/static`),
    headers: {'Access-Control-Allow-Origin': '*'},
    host: '0.0.0.0',
    port: 8090,
    hot: true,
    inline: true,
    clientLogLevel: 'silent'
  },
  plugins: [
    new VueLoaderPlugin(),
    new CleanWebpackPlugin(),
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery'
    }),
    new MiniCssExtractPlugin({filename: '[name].css'}),
  ],
}

const isDevelopmentMode = process.env.NODE_ENV !== 'prod';
if (isDevelopmentMode) {
  config.mode = 'development';
  config.devtool = 'eval-source-map';
  config.output.filename = '[name].bundle.js';
  config.output.publicPath = 'http://localhost:8090/assets/';
} else {
  config.plugins.push(
    new SentryWebpackPlugin({
      authToken: 'ad1dea680dac46859cd380b7e18ed48769af9779fcc648d1844d3035e002e6e6',
      org: 'eahub',
      project: 'eahub-front',
      include: '.',
      ignore: ['node_modules', 'webpack.config.js'],
      release: '1.0.0',
    }),
  )
}

const isDockerMode = process.env.NODE_ENV === 'docker';
if (isDockerMode) {
  config.devServer.watchOptions = {
    poll: 100, // enable polling since fsevents are not supported in docker
  }
}

module.exports = config;
