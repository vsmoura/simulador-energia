module.exports = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
  transform: {
    "^.+\\.(ts|tsx)$": [
      "ts-jest",
      {
        tsconfig: "tsconfig.app.json",
        useESM: true,
      },
    ],
  },
  moduleNameMapper: {
    "\\.(css|less|scss)$": "<rootDir>/src/tests/styleMock.ts",
  },
  extensionsToTreatAsEsm: [".ts", ".tsx"],
};
