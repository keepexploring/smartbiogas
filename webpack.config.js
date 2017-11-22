var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ip = 'localhost'

module.exports = {
    context: __dirname,
    entry: {
        App: './reactjs/js/index.jsx'
           },
    output: {
        path: path.resolve('./assets/bundles/'),
        publicPath: '/assets/bundles/'
        filename: "[name]-[hash].js"
    }
,
config.output.publicPath = 'http://' + ip + ':3000' + '/assets/bundles/'

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
<<<<<<< HEAD
=======
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
          
>>>>>>> 46a7498c2dde1048bd30e656122b76ac71cce659
          }
            
        ]
    }
};
