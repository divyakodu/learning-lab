const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.RESUME_APP_URL || "http://localhost:8080",
    supportFile: false,
  },
});
