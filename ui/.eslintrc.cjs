module.exports = {
  root: true,
  env: {
    browser: true,
    es2020: true,
    // vite.config.ts reads `process.env.VITE_API_URL`, which is a Node
    // global, not a browser one. Without this, eslint:recommended's
    // no-undef rule would flag `process` as undefined when linting that file.
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended",
  ],
  ignorePatterns: ["dist", ".eslintrc.cjs", "node_modules"],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    ecmaFeatures: { jsx: true },
  },
  plugins: ["@typescript-eslint", "react-hooks", "react-refresh"],
  rules: {
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": "warn",
  },
};
