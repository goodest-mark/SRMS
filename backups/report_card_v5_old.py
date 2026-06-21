from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet

from database import connect


def generate_report_book(
    parent,
    exam_id,
    class_name,
    save_path
):
    try:

        conn = connect()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            school_name,
            school_address,
            school_phone,
            school_email
        FROM school_profile
        LIMIT 1
        """)

        school = cur.fetchone()

        school_name = school[0] if school else "SRMS SCHOOL"
        school_address = school[1] if school else ""
        school_phone = school[2] if school else ""
        school_email = school[3] if school else ""

        doc = SimpleDocTemplate(
            save_path,
            pagesize=landscape(A4),
            leftMargin=25,
            rightMargin=25,
            topMargin=20,
            bottomMargin=20
        )

        styles = getSampleStyleSheet()
        elements = []

        title_style = styles["Title"]
        normal = styles["BodyText"]

        elements.append(
            Paragraph(
                school_name,
                title_style
            )
        )

        elements.append(
            Paragraph(
                f"{school_address} | {school_phone} | {school_email}",
                normal
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                "ACADEMIC REPORT CARD",
                title_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        sample_student = [
            ["Student Name", "Sample Student"],
            ["Admission No", "ADM001"],
            ["Gender", "Male"],
            ["Class", class_name]
        ]

        info_table = Table(
            sample_student,
            colWidths=[120, 250]
        )

        info_table.setStyle(
            TableStyle([
                ("GRID",(0,0),(-1,-1),1,colors.black),
                ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),
            ])
        )

        elements.append(info_table)

        doc.build(elements)

        conn.close()

        return True, "SRMS V5 Report Card Generated"

    except Exception as e:
        return False, str(e)

