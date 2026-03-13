const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const sass = require('sass');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const options = {
    entry: {
        // multiple entries can be added here
        // 'main' is ignored from prettier because if vue (or anything else) isn't added
        // here, it will deem the quotes uneccessary.
        'main': `./static_src/javascript/main.js`, // prettier-ignore
    },
    resolve: {
        extensions: ['.js'],
    },
    output: {
        path: path.resolve(`./static_compiled/`),
        // based on entry name, e.g. main.js
        filename: 'js/[name].js', // based on entry name, e.g. main.js
    },
    plugins: [
        new CopyPlugin({
            patterns: [
                // Copy images to be referenced directly by Django to the "images" subfolder in static files.
                // Ignore CSS background images as these are handled separately below
               {
                from: path.resolve(`./static_src/images`),
                to: path.resolve(`./static_compiled/images`),
               }
            ],
        }),
        new MiniCssExtractPlugin({
            filename: 'css/[name].css',
        }),
        //  Automatically remove all unused webpack assets on rebuild
        new CleanWebpackPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.(scss|css)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true,
                        },
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true,
                            postcssOptions: {
                                plugins: [
                                    'tailwindcss',
                                    'autoprefixer',
                                    'postcss-custom-properties',
                                    ['cssnano', { preset: 'default' }],
                                ],
                            },
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                            implementation: sass,
                            sassOptions: {
                                outputStyle: 'compressed',
                            },
                        },
                    },
                ],
            },
            {
                test: /\.(ttf|woff|woff2)$/,
                exclude: /node_modules/,
                type: 'asset/resource',
                generator: {
                  filename: 'fonts/[name][ext]'
                }
              }
        ],
    },
    // externals are loaded via base.html and not included in the webpack bundle.
    externals: {
        // gettext: 'gettext',
    },
};

const webpackConfig = (environment, argv) => {
    const isProduction = argv.mode === 'production';

    options.mode = isProduction ? 'production' : 'development';

    if (!isProduction) {
        // https://webpack.js.org/configuration/stats/
        const stats = {
            // Tells stats whether to add the build date and the build time information.
            builtAt: false,
            // Add chunk information (setting this to `false` allows for a less verbose output)
            chunks: false,
            // Add the hash of the compilation
            hash: false,
            // `webpack --colors` equivalent
            colors: true,
            // Add information about the reasons why modules are included
            reasons: false,
            // Add webpack version information
            version: false,
            // Add built modules information
            modules: false,
            // Show performance hint when file size exceeds `performance.maxAssetSize`
            performance: false,
            // Add children information
            children: false,
            // Add asset Information.
            assets: false,
        };

        options.stats = stats;

        // Create JS source maps in the dev mode
        // See https://webpack.js.org/configuration/devtool/ for more options
        options.devtool = 'inline-source-map';

        // See https://webpack.js.org/configuration/dev-server/.
        options.devServer = {
            // Enable gzip compression for everything served.
            compress: true,
            // Shows a full-screen overlay in the browser when there are compiler errors.
            overlay: true,
            clientLogLevel: 'error',
            contentBase: false,
            // Write compiled files to disk. This makes live-reload work on both port 3000 and 8000.
            writeToDisk: true,
            host: '0.0.0.0',
            allowedHosts: [],
            port: 3000,
            publicPath: '/static/',
            index: '',
            stats,
            proxy: {
                context: () => true,
                target: 'http://localhost:8000',
            },
        };
    }

    return options;
};

module.exports = webpackConfig;
