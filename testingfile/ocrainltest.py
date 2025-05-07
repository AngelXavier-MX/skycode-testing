from locust import HttpUser, task, between
import os

class DocumentOCRUser(HttpUser):
    wait_time = between(1, 3)

    def upload_document(self, file_path, mime_type, operation, endpoint):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f, mime_type)
            }

            data = {
                "operation": operation,
                "endpoint": endpoint
            }

            response = self.client.post(
                "/components_proxy_api/",
                files=files,
                data=data
            )

            print(f"Status Code: {response.status_code}")
            print(response.text)

    @task(1)
    def run_aadhar_extraction(self):
        self.upload_document("test_files/aadar.jpg", "image/jpg", "AdharExtraction", "AadharcardExtractionView/")

    @task(1)
    def run_pan_extraction(self):
        self.upload_document("test_files/pan.jpg", "image/jpg", "PanExtraction", "PancardExtractionView/")

    @task(1)
    def run_qr_extraction(self):
        self.upload_document("test_files/qr.png", "image/png", "Decode", "OCRExtractionView/")

    @task(1)
    def run_pdf_extraction(self):
        self.upload_document(
            file_path="test_files/angel.pdf",
            mime_type="application/pdf",
            operation="PDFExtraction",
            endpoint="OCRExtractionView/"
        )

    @task(1)
    def run_invoice_extraction(self):
        self.upload_document(
            file_path="test_files/invoice.pdf",  # Replace with your actual invoice file
            mime_type="application/pdf",
            operation="InvoiceExtraction",
            endpoint="OCRExtractionView/"
        )

