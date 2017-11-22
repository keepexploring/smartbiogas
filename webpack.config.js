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
          }
            
        ]
    }
};
