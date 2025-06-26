module.exports = {
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^react-router-dom$': require.resolve('react-router-dom'),
  },
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },
};
