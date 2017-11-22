var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ip = 'localhost';

module.exports = {
    context: __dirname,
    entry: {
        App: './reactjs/js/index.jsx'
           },
    output: {
        path: path.resolve('./assets/bundles/'),
        // publicPath: '/Users/Joel/Documents/CREATIVenergie/Dashboard2/django_react3/SimpleReactDjango/assets/bundles/',
        filename: "[name]-[hash].js"
    }
,

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],

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
          {
            test: /\.(jpe?g|png|gif|svg|tif)$/,
            loader: "file-loader"
          
          }
            
        ]
    }
};
