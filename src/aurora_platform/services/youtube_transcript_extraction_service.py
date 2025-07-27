import os
import subprocess
import logging
import json
from typing import List

from aurora_platform.services.audio_transcription_service import (
    AudioTranscriptionService,
)

logger = logging.getLogger(__name__)


class YoutubeTranscriptExtractionService:
    def __init__(self, project_name: str, ordem_servico_id: str):
        self.project_name = project_name
        self.ordem_servico_id = ordem_servico_id
        self.workspace_dir = os.path.join(
            "data", "projetos", project_name, "youtube", ordem_servico_id
        )
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.fallback_report = []
        # Compatibilidade com testes: caminhos esperados
        self.video_urls_file = os.path.join(self.workspace_dir, "video_urls.txt")
        self.fallback_report_file = os.path.join(
            self.workspace_dir, "fallback_report.json"
        )

    def discover_video_urls(self, channel_url: str) -> List[str]:
        """Usa yt-dlp para listar todas as URLs dos vídeos do canal."""
        output_path = os.path.join(self.workspace_dir, "video_urls.txt")
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--get-url",
            channel_url,
        ]
        logger.info(f"[OS-{self.ordem_servico_id}] Executando: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            urls = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            with open(output_path, "w", encoding="utf-8") as f:
                for url in urls:
                    f.write(url + "\n")
            logger.info(
                f"[OS-{self.ordem_servico_id}] {len(urls)} URLs salvas em {output_path}"
            )
            return urls
        except subprocess.CalledProcessError as e:
            logger.error(f"[OS-{self.ordem_servico_id}] Erro yt-dlp: {e.stderr}")
            return []

    def extract_transcripts_from_channel(self, channel_url: str):
        video_urls = self.discover_video_urls(channel_url)
        if not video_urls:
            logger.warning(f"[OS-{self.ordem_servico_id}] Nenhum vídeo encontrado.")
            return

        summary = {
            "total_videos": len(video_urls),
            "success": 0,
            "fallback": 0,
            "failed": 0,
        }
        for url in video_urls:
            video_id = url.split("v=")[-1] if "v=" in url else url.split("/")[-1]
            log_path = os.path.join(self.workspace_dir, f"transcript_{video_id}.log")
            transcript_txt_path = os.path.join(
                self.workspace_dir, f"transcript_{video_id}.txt"
            )


            try:
                cmd = [
                    "yt-dlp",
                    "--skip-download",
                    "--write-subs",
                    "--sub-langs",
                    "pt,pt-BR,en",
                    "--convert-subs",
                    "srt",
                    "-o",
                    os.path.join(self.workspace_dir, "%(id)s.%(ext)s"),
                    url,
                ]
                logger.info(
                    f"[OS-{self.ordem_servico_id}] Baixando legendas: {' '.join(cmd)}"
                )
                subprocess.run(cmd, capture_output=True, text=True, check=True)

                transcript = ""
                found = False
                for lang in ["pt", "pt-BR", "en"]:
                    srt_try = os.path.join(self.workspace_dir, f"{video_id}.{lang}.srt")
                    if os.path.exists(srt_try):
                        with open(srt_try, "r", encoding="utf-8") as f:
                            transcript = self.srt_to_text(f.read())
                        os.remove(srt_try)
                        found = True
                        break

                if found:
                    with open(transcript_txt_path, "w", encoding="utf-8") as f:
                        f.write(transcript)
                    summary["success"] += 1
                    self._log(
                        log_path, "success", url, "Transcrição extraída com sucesso."
                    )
                else:
                    # Fallback para áudio
                    logger.warning(
                        f"[OS-{self.ordem_servico_id}] Sem legendas em {url}, iniciando fallback por áudio."
                    )
                    summary["fallback"] += 1
                    transcript = AudioTranscriptionService().transcribe_audio(url)
                    if transcript:
                        with open(transcript_txt_path, "w", encoding="utf-8") as f:
                            f.write(transcript)
                        self._log(
                            log_path,
                            "fallback",
                            url,
                            "Transcrição via áudio (fallback).",
                        )
                    else:
                        summary["failed"] += 1
                        self.fallback_report.append(
                            {"video_url": url, "status": "failed"}
                        )
                        self._log(
                            log_path, "failed", url, "Transcrição falhou totalmente."
                        )
            except Exception as e:
                logger.error(f"[OS-{self.ordem_servico_id}] Falha no vídeo {url}: {e}")
                summary["failed"] += 1
                self.fallback_report.append({"video_url": url, "status": "failed"})
                self._log(log_path, "error", url, str(e))

        # Salva fallback_report e summary_report
        with open(
            os.path.join(self.workspace_dir, "fallback_report.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(self.fallback_report, f, ensure_ascii=False, indent=2)
        with open(
            os.path.join(self.workspace_dir, "summary_report.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        logger.info(f"[OS-{self.ordem_servico_id}] Processamento concluído: {summary}")

    def srt_to_text(self, srt_content: str) -> str:
        """Remove cabeçalhos numéricos e timestamps do SRT, retorna texto puro."""
        text_lines = []
        for line in srt_content.split("\n"):
            if not line.strip().isdigit() and "-->" not in line:
                text_lines.append(line.strip())
        return " ".join(text_lines).replace("  ", " ")

    def _log(self, log_path, status, url, message):
        with open(log_path, "a", encoding="utf-8") as logf:
            logf.write(f"{status.upper()} | {url} | {message}\n")
