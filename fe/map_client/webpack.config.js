const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
    entry: path.join(__dirname, "src", "index.js"),
    output: {
        path: path.join(__dirname, "build"),
        filename: "index.bundle.js"
    },
    externals: {
        'configurations': JSON.stringify(require('../../configurations.json'))
    },
    mode: process.env.NODE_ENV || "development",
    resolve: {
        modules: [
            path.resolve(__dirname, "src"),
            "node_modules"]
    },
    devServer: {contentBase: path.join(__dirname, "src")},
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            },
            {
                test: /\.(jpg|jpeg|png|gif|mp3|svg|woff2|eot|woff|ttf)$/,
                use: ["file-loader"]
            },
            {
                test: /\.(scss|css)$/,
                use: ['style-loader', 'css-loader', 'sass-loader'],
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(__dirname, "src", "index.html"),
        }),
    ],
};