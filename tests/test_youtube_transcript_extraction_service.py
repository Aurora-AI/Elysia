import os
import pytest
from aurora_platform.services.youtube_transcript_extraction_service import YoutubeTranscriptExtractionService

def test_extract_transcripts_from_channel(tmp_path):
    # Setup
    project_name = "test_project"
    ordem_servico_id = "os_test_001"
    workspace = tmp_path / project_name / "youtube" / ordem_servico_id
    workspace.mkdir(parents=True, exist_ok=True)
    service = YoutubeTranscriptExtractionService(
        project_name=project_name,
        ordem_servico_id=ordem_servico_id
    )
    # Canal de teste com poucos vídeos e legendas automáticas
    channel_url = "https://www.youtube.com/@ronnaldhawk"
    service.extract_transcripts_from_channel(channel_url)
    # Verificações
    assert os.path.exists(service.video_urls_file)
    with open(service.video_urls_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    assert len(urls) > 0
    # Fallback report deve existir
    assert os.path.exists(service.fallback_report_file)
    # Pelo menos um arquivo de transcrição ou fallback
    transcript_files = list(workspace.glob("transcript_*.txt"))
    assert len(transcript_files) > 0 or os.path.getsize(service.fallback_report_file) > 0
