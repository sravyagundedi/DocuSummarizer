import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def build_pdf_report(result, source_name):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("ReportTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=20)
    story = [Paragraph("DocuSummarizer", title), Paragraph(f"Meeting: {source_name}", styles["BodyText"]),
             Spacer(1, 12), Paragraph("Executive Summary", styles["Heading2"]),
             Paragraph(result["summary"], styles["BodyText"]), Spacer(1, 10)]
    story.append(Paragraph("Key Decisions", styles["Heading2"]))
    for x in result["decisions"]:
        story += [Paragraph(f"<b>{x['decision']}</b><br/>Speaker: {x['speaker']}<br/>{x.get('evidence','')}", styles["BodyText"]), Spacer(1, 6)]
    story.append(Paragraph("Action Items", styles["Heading2"]))
    rows = [["Action", "Owner", "Deadline"]] + [[x["action"], x.get("owner") or "Not specified", x.get("deadline") or "Not specified"] for x in result["actions"]]
    table = Table(rows, repeatRows=1, colWidths=[270, 110, 100])
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1F3A5F")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.5,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("FONTSIZE",(0,0),(-1,-1),8)]))
    story += [table, Spacer(1, 12), Paragraph("Risk Flags", styles["Heading2"])]
    for x in result["risks"]:
        story += [Paragraph(f"<b>{x['severity'].upper()}: {x['risk']}</b><br/>Owner: {x.get('owner') or 'Not specified'}<br/>{x.get('evidence','')}", styles["BodyText"]), Spacer(1, 6)]
    story.append(Paragraph("Topic Clusters", styles["Heading2"]))
    for x in result["topics"]:
        story += [Paragraph(f"<b>{x['topic']}</b>: {x['description']}", styles["BodyText"]), Spacer(1, 5)]
    u = result["usage"]
    story += [Paragraph("Token Usage", styles["Heading2"]), Paragraph(f"Input: {u['input_tokens']} | Output: {u['output_tokens']} | Calls: {u['calls']} | Estimated cost: ${u['estimated_cost_usd']:.6f}", styles["BodyText"])]
    doc.build(story)
    return buffer.getvalue()
