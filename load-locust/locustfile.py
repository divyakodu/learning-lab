from locust import HttpUser, between, task

SLUG = "divya-kodukula"


class ResumeAppUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(10)
    def view_list(self):
        self.client.get("/api/resumes", name="/api/resumes")

    @task(6)
    def view_detail(self):
        self.client.get(f"/api/resumes/{SLUG}", name="/api/resumes/[slug]")

    @task(2)
    def download_pdf(self):
        self.client.get(f"/api/resumes/{SLUG}/pdf", name="/api/resumes/[slug]/pdf")

    @task(1)
    def download_docx(self):
        self.client.get(f"/api/resumes/{SLUG}/docx", name="/api/resumes/[slug]/docx")

    @task(1)
    def health(self):
        self.client.get("/api/health", name="/api/health")
