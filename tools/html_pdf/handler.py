import os

def generate_pdf_or_html(html: str, filename: str):
    """
    Fallback approach:
    - Try converting to PDF using wkhtmltopdf (if installed)
    - If not available (e.g., Kaggle), save HTML only
    """

    # Save HTML file always
    html_path = os.path.join(os.getcwd(), filename.replace(".pdf", ".html"))
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Try PDF generation
    try:
        import pdfkit
        config = pdfkit.configuration()
        pdf_path = os.path.join(os.getcwd(), filename)

        pdfkit.from_string(html, pdf_path, configuration=config)

        return {
            "status": "pdf_generated",
            "html_path": html_path,
            "pdf_file_path": pdf_path,
            "mode": "pdf+html"
        }

    except Exception:
        # Fallback: HTML only
        return {
            "status": "html_only",
            "html_path": html_path,
            "pdf_file_path": None,
            "mode": "html-only"
        }


def main(function: str, args: dict):
    if function == "generate_pdf_or_html":
        return generate_pdf_or_html(args["html"], args["filename"])
    else:
        return {"error": "unknown function"}

