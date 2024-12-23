import os
import time
from mutagen.mp3 import MP3
from TTS.engine_wrapper import TTSEngine
from TTS.TikTok import TikTok
import traceback

# Mapeamento de provedores TTS
TTSProviders = {
    # "GoogleTranslate": GTTS,
    # "AWSPolly": AWSPolly,
    # "StreamlabsPolly": StreamlabsPolly,
    "TikTok": TikTok,
    # "pyttsx": pyttsx,
    # "ElevenLabs": elevenlabs,
}

# Função para calcular o comprimento do arquivo MP3
def get_mp3_length(file_path):
    # Esperar até que o arquivo seja salvo
    while not os.path.exists(file_path):
        time.sleep(0.1)
    audio = MP3(file_path)
    return audio.info.length

# Função para gerar o áudio usando TTSEngine
def makeTTS(dict):
    length = 0

    # Configuração do provedor de TTS
    voice = "TikTok"
    try:
        text_to_mp3 = TTSEngine(TTSProviders[voice], dict, path=f"/steam/assets/{dict['thread_id']}")
        # Gerar o áudio
        text_to_mp3.run()
    except Exception as e:
        error_message = traceback.format_exc()  # Extrai o traceback completo como uma string
        raise Exception(f"Erro (nessa parte normalmente é porque o session_id do tiktok está invalido mude a env TIKTOK_SESSION): {e}\nDetalhes do erro:\n{error_message}")
    # Retornar o comprimento do áudio
    return 1
