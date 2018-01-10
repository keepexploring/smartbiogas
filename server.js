var webpack = require('webpack')
var WebpackDevServer = require('webpack-dev-server')
var config = require('./webpack.local.config')

const ip = '127.0.0.1'

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  inline: true,
  historyApiFallback: true,
}).listen(3000, ip, function (err, result) {
  if (err) {
    console.log(err)
  }
  console.log('Listening at ' + ip + ':3000')
})
