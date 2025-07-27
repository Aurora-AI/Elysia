import logging

logger = logging.getLogger(__name__)

class AudioTranscriptionService:
    def transcribe_audio(self, video_url: str) -> str:
        """
        Fallback de transcrição por áudio. Implementação real deve baixar o áudio,
        processar com modelo de STT (ex: Whisper) e retornar o texto.
        Aqui retorna texto simulado para integração e testes.
        """
        logger.info(f"[AUDIO-FALLBACK] Iniciando transcrição por áudio para: {video_url}")
        # Simulação: sempre retorna um texto de exemplo
        return f"[Transcrição simulada para: {video_url}]"
