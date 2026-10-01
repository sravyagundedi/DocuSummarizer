import json
import streamlit as st
from app.config import settings
from app.ingestion import ingest_uploaded_file
from app.pipeline import DocuSummarizer
from app.exporters import build_pdf_report

st.set_page_config(page_title="DocuSummarizer", page_icon="📝", layout="wide")
st.title("📝 DocuSummarizer")
st.caption("AI-Powered Meeting Intelligence Platform")

with st.sidebar:
    st.header("Pipeline")
    st.write("Provider:", settings.llm_provider)
    st.write("Model:", settings.model_name)
    st.write("Max transcript:", f"{settings.max_transcript_words:,} words")

uploaded = st.file_uploader("Upload a meeting transcript", type=["txt", "docx", "pdf"])
if uploaded and st.button("Analyze meeting", type="primary", use_container_width=True):
    try:
        bar = st.progress(0, text="Reading transcript...")
        text = ingest_uploaded_file(uploaded)
        bar.progress(15, text="Preparing speaker-aware chunks...")
        result = DocuSummarizer(settings).run(text, progress_callback=lambda p,m: bar.progress(p, text=m))
        st.session_state["result"] = result
        st.session_state["source"] = uploaded.name
        st.success("Analysis completed.")
    except Exception as e:
        st.error(str(e))

if "result" in st.session_state:
    result = st.session_state["result"]
    source = st.session_state["source"]
    t1,t2,t3,t4,t5,t6,t7 = st.tabs(["Summary","Decisions","Actions","Risks","Topics","Usage","Raw JSON"])
    with t1: st.write(result["summary"])
    with t2:
        for x in result["decisions"]:
            st.container(border=True).write(f"**{x['decision']}** — {x['speaker']}\n\n{x.get('evidence','')}")
    with t3:
        for x in result["actions"]:
            st.container(border=True).write(f"**{x['action']}**\nOwner: {x.get('owner') or 'Not specified'}\nDeadline: {x.get('deadline') or 'Not specified'}")
    with t4:
        for x in result["risks"]:
            st.container(border=True).write(f"**{x['severity'].upper()}** — {x['risk']}\nOwner: {x.get('owner') or 'Not specified'}")
    with t5:
        for x in result["topics"]:
            st.write(f"**{x['topic']}** — {x['description']}")
    with t6: st.json(result["usage"])
    with t7: st.json(result)

    st.download_button("Download JSON", json.dumps(result, indent=2), f"{source}_analysis.json", "application/json", use_container_width=True)
    st.download_button("Download PDF Report", build_pdf_report(result, source), f"{source}_report.pdf", "application/pdf", use_container_width=True)
else:
    st.info("Upload a transcript to begin.")
