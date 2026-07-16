const KNOWN_SLUG = "divya-kodukula";

describe("resume list", () => {
  it("shows the known resume", () => {
    cy.visit("/index.html");
    cy.get('[data-testid="resume-list"]').should("be.visible");
    cy.get(`[data-testid="resume-link-${KNOWN_SLUG}"]`).should("be.visible");
  });

  it("navigates to the detail page on click", () => {
    cy.visit("/index.html");
    cy.get(`[data-testid="resume-link-${KNOWN_SLUG}"]`).click();
    cy.url().should("include", `slug=${KNOWN_SLUG}`);
    cy.get('[data-testid="resume-name"]').should("have.text", "Divya Kodukula");
  });
});
