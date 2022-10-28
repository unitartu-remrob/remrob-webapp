module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true
            },
            '/containers': {
                target: 'http://localhost:9000',
                changeOrigin: true,
                pathRewrite: {'/containers': '/'},
            }
        }
    }
}