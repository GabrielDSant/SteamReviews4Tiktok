import os
import shutil
import ffmpeg
import openai
import whisper
from tiktok_uploader.upload import upload_video
import subprocess
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "/usr/bin/google-chrome"  # Caminho para o binário do Google Chrome
options.add_argument("--headless")  # Executar no modo headless (opcional)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


# options = {
#     "chrome_binary": "/usr/bin/google-chrome",
#     "chromedriver_binary": "/usr/local/bin/chromedriver",
#     "headless": True,  # Executa o Chrome sem interface gráfica
#     "disable-gpu": True,  # Necessário em alguns ambientes Linux
#     "no-sandbox": True,  # Evita erros de permissão
#     "disable-dev-shm-usage": True  # Usa espaço no disco em vez de /dev/shm
# }

# Configurações
openai.api_key = ''
TAG_FIXAS = "#steam #meme #geek #gamesreview #funny #engraçado"

# Função para extrair áudio do vídeo
def extrair_audio(video_path, audio_path):
    ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)

# Função para transcrever o áudio
def transcrever_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']

# Função para gerar descrição
def gerar_descricao(texto):
    prompt = f"Resuma o seguinte conteúdo para uma descrição curta: {texto}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Você é um assistente que cria descrições curtas."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# Função para upload no TikTok
def upload_tiktok(video_path, descricao):
    upload_video(video_path, description=descricao + " " + TAG_FIXAS, cookies="cookies.txt", options=options)

# Função para mover vídeo após envio
def mover_video(video_path, tema):
    destino = os.path.join(PASTA_ENVIADOS, tema)
    os.makedirs(destino, exist_ok=True)
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
                print(f"Arquivo inválido ou corrompido: {video_path}")
                continue

            audio_path = video_path.replace(".mp4", ".mp3")
            extrair_audio(video_path, audio_path)
            transcricao = transcrever_audio(audio_path)
            descricao = gerar_descricao(transcricao)

            upload_tiktok(video_path, descricao)
            # mover_video(video_path, "enviados")

            os.remove(video_path)  # Limpa o áudio gerado
            os.remove(audio_path)  # Limpa o áudio gerado

# Executa o script
processar_videos('/resultados/steam')
