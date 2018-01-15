var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: {
        Dashboard: './reactjs/js/Dashboard.jsx',
        Technicians: './reactjs/js/Technicians.jsx',
        Jobs: './reactjs/js/Jobs.jsx',
        Plants: './reactjs/js/Jobs.jsx',
           },
    output: {
        path: path.resolve('./assets/bundles/'),
        filename: "[name]-[hash].js"
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],
    devServer: {
        headers: {
          'Access-Control-Allow-Origin': '*',
        },
      },
    module: {
        loaders: [
            {
                test: /\.jsx$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                  loader: 'babel-loader',
                  options: {
                    presets: ['react','es2015','env']
                  }
                }
              },
              {
            test: /\.scss$/,
            use: [{
                loader: "style-loader" // creates style nodes from JS strings
            }, {
                loader: "css-loader" // translates CSS into CommonJS
            }, {
                loader: "sass-loader" // compiles Sass to CSS
            }]
          },
          { test: /\.css$/, loader: "style-loader!css-loader" },
            {
             test: /\.(png|jpg|gif)$/,
             use: [
               {
                 loader: 'file-loader',
                 options: {}
               }
             ]
           }
        ]
    }
};
