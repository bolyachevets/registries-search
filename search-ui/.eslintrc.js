module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/typescript/recommended',
    // 'plugin:prettier/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    'max-len': ['warn', { code: 120, ignoreRegExpLiterals: true, ignoreTrailingComments: true }],
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    '@typescript-eslint/no-explicit-any': 'off',
    // 'prettier/prettier': [
    //   'warn',
    //   {
    //     arrowParens: 'avoid',
    //     endOfLine: 'lf',
    //     jsxBracketSameLine: false,
    //     printWidth: 80,
    //     proseWrap: 'never',
    //     quoteProps: 'as-needed',
    //     singleQuote: true,
    //     semi: false,
    //     trailingComma: 'es5',
    //     useTabs: false,
    //     vueIndentScriptAndStyle: false,
    //   },
    // ],
  },
  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)',
      ],
      env: {
        jest: true,
      },
    },
  ],
}
