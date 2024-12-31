import os
import shutil
import ffmpeg
import openai
import whisper
from tiktok_uploader.upload import upload_video as upload_tiktok_video
from youtube_shorts_upload import upload_video as upload_youtube_video
import subprocess
from selenium.webdriver.chrome.options import Options
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

options = Options()
options.binary_location = "/usr/bin/google-chrome"  # Caminho para o binário do Google Chrome
options.add_argument("--headless")  # Executar no modo headless (opcional)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Configurações
openai.api_key = 'XXXXXXXXXXXXXXXXXXX'
TAG_FIXAS = "#steam #meme #geek #gamesreview #funny #engraçado"

# Função para extrair áudio do vídeo
def extrair_audio(video_path, audio_path):
    logging.info(f"Extraindo áudio de {video_path} para {audio_path}")
    ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)

# Função para transcrever o áudio
def transcrever_audio(audio_path):
    logging.info(f"Transcrevendo áudio {audio_path}")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']

# Função para gerar descrição
def gerar_descricao(texto):
    logging.info("Gerando descrição")
    prompt = f"Resuma o seguinte conteúdo para uma descrição curta: {texto}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente que cria descrições curtas."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# Função para upload no TikTok
def upload_tiktok(video_path, descricao):
    logging.info(f"Fazendo upload para TikTok: {video_path}")
    upload_tiktok_video(video_path, description=descricao + " " + TAG_FIXAS, cookies="cookies.txt", options=options)

# Função para upload no YouTube Shorts
def upload_youtube(video_path, descricao):
    logging.info(f"Fazendo upload para YouTube Shorts: {video_path}")
    title = os.path.splitext(os.path.basename(video_path))[0]
    tags = ["shorts", "YouTubeShorts", "steam", "meme", "geek", "gamesreview", "funny", "engraçado"]
    response = upload_youtube_video(video_path, title, descricao, tags)
    logging.info(f"Upload para YouTube Shorts concluído: {response['id']}")

# Função para mover vídeo após envio
def mover_video(video_path, tema):
    destino = os.path.join(PASTA_ENVIADOS, tema)
    os.makedirs(destino, existok=True)
    shutil.move(video_path, os.path.join(destino, os.path.basename(video_path)))

def verificar_video(video_path):
    try:
        subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1', video_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False

# Função principal
def processar_videos(diretorio_principal):
    for arquivo in os.listdir(diretorio_principal):
        if arquivo.endswith(".mp4"):
            video_path = os.path.join(diretorio_principal, arquivo)
            
            if not verificar_video(video_path):
                logging.error(f"Arquivo inválido ou corrompido: {video_path}")
                continue

            audio_path = video_path.replace(".mp4", ".mp3")
            extrair_audio(video_path, audio_path)
            transcricao = transcrever_audio(audio_path)
            descricao = gerar_descricao(transcricao)

            # upload_tiktok(video_path, descricao)
            upload_youtube(video_path, descricao)
            # mover_video(video_path, "enviados")

            # os.remove(video_path)  # Limpa o áudio gerado
            os.remove(audio_path)  # Limpa o áudio gerado

# Executa o script
if __name__ == "__main__":
    logging.info("Iniciando processamento de vídeos")
    processar_videos('/resultados/steam')
    logging.info("Processamento de vídeos concluído")
