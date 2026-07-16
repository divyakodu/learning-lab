Feature: Resume list and detail
  As a visitor
  I want to browse and download resumes
  So that I can view someone's experience in the format I prefer

  Scenario: Browsing the resume list
    When I open the resume list
    Then I should see a link for "divya-kodukula"

  Scenario: Viewing a resume's detail page
    When I open the resume detail page for "divya-kodukula"
    Then I should see the name "Divya Kodukula"

  Scenario: Viewing an unknown resume
    When I open the resume detail page for "does-not-exist"
    Then I should see a not-found message

  Scenario: Downloading a PDF
    When I download the PDF for "divya-kodukula"
    Then the downloaded file should be a valid PDF

  Scenario: Downloading a DOCX
    When I download the DOCX for "divya-kodukula"
    Then the downloaded file should be a valid DOCX
