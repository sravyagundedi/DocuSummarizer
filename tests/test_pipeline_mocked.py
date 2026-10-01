def test_pipeline_module_imports():
    from app.pipeline import DocuSummarizer
    assert DocuSummarizer is not None
