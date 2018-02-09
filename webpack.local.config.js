var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var ip = '127.0.0.1';
var config = require('./webpack.config.js');

config.entry = {
  App: [
    'webpack-dev-server/client?http://' + ip + ':3000',
    'webpack/hot/only-dev-server',
    './reactjs/Main.jsx',
  ]
};

config.output.publicPath = 'http://' + ip + ':3000' + '/assets/bundles/';

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(),
  new BundleTracker({ filename: './webpack-stats.json' }),
]);

config.devtool = 'cheap-module-source-map';

module.exports = config;
