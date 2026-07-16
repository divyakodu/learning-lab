const path = require("path");

const KNOWN_SLUG = "divya-kodukula";

describe("downloads", () => {
  it("PDF download button produces a real PDF", () => {
    cy.visit(`/resume.html?slug=${KNOWN_SLUG}`);
    cy.get('[data-testid="download-pdf"]').click();
    const downloadsFolder = Cypress.config("downloadsFolder");
    cy.readFile(path.join(downloadsFolder, `${KNOWN_SLUG}.pdf`), "binary", { timeout: 10000 }).should(
      (content) => {
        expect(content.slice(0, 4)).to.eq("%PDF");
      }
    );
  });

  it("DOCX download button produces a real DOCX", () => {
    cy.visit(`/resume.html?slug=${KNOWN_SLUG}`);
    cy.get('[data-testid="download-docx"]').click();
    const downloadsFolder = Cypress.config("downloadsFolder");
    cy.readFile(path.join(downloadsFolder, `${KNOWN_SLUG}.docx`), "binary", { timeout: 10000 }).should(
      (content) => {
        expect(content.slice(0, 2)).to.eq("PK"); // docx is a zip container
      }
    );
  });
});
