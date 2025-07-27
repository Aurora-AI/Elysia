import os
import pytest
from aurora_platform.services.youtube_transcript_extraction_service import YoutubeTranscriptExtractionService

@pytest.mark.asyncio
async def test_youtube_transcript_extraction(tmp_path):
    project_name = "test_project"
    ordem_servico_id = "os_test_001"
    channel_url = "https://www.youtube.com/@ronnaldhawk"

    service = YoutubeTranscriptExtractionService(
        project_name=project_name, ordem_servico_id=ordem_servico_id
    )
    service.extract_transcripts_from_channel(channel_url=channel_url)

    ws_dir = os.path.join(
        "data", "projetos", project_name, "youtube", ordem_servico_id
    )

    assert os.path.exists(os.path.join(ws_dir, "video_urls.txt"))
    transcripts = [f for f in os.listdir(ws_dir) if f.startswith("transcript_") and f.endswith(".txt")]
    assert len(transcripts) > 0
    assert os.path.exists(os.path.join(ws_dir, "fallback_report.json"))
    assert os.path.exists(os.path.join(ws_dir, "summary_report.json"))
