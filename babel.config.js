module.exports = {
  presets: [
    '@babel/preset-env',
    '@babel/preset-react',  // Для роботи з React, якщо використовуєте
  ],
  plugins: [
    '@babel/plugin-transform-modules-commonjs', // Це допоможе перетворити ваші модулі в CommonJS
  ],
};
