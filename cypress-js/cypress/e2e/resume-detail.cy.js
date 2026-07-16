const KNOWN_SLUG = "divya-kodukula";

describe("resume detail", () => {
  it("shows name, headline, and summary", () => {
    cy.visit(`/resume.html?slug=${KNOWN_SLUG}`);
    cy.get('[data-testid="resume-name"]').should("have.text", "Divya Kodukula");
    cy.get('[data-testid="resume-headline"]').should("not.be.empty");
    cy.get('[data-testid="resume-summary"] li').should("have.length.greaterThan", 0);
  });

  it("back link returns to the resume list", () => {
    cy.visit(`/resume.html?slug=${KNOWN_SLUG}`);
    cy.get('[data-testid="back-link"]').click();
    cy.url().should("include", "index.html");
    cy.get('[data-testid="resume-list"]').should("be.visible");
  });

  it("shows a not-found message for an unknown slug", () => {
    cy.visit("/resume.html?slug=does-not-exist");
    cy.get('[data-testid="resume-name"]').should("have.text", "Resume not found");
  });
});
