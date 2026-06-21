from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report_book(
    parent,
    exam_id,
    class_name,
    save_path
):
    try:

        doc = SimpleDocTemplate(
            save_path,
            pagesize=landscape(A4)
        )

        styles = getSampleStyleSheet()

        elements = [
            Paragraph(
                "SRMS V5 REPORT CARD ENGINE",
                styles["Title"]
            )
        ]

        doc.build(elements)

        return True, "V5 Report Card Created"

    except Exception as e:
        return False, str(e)

