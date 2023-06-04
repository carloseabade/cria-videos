from moviepy.editor import ImageClip, concatenate_videoclips, CompositeVideoClip
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip
from PIL import ImageFont, ImageDraw, Image
import os
import numpy as np
from moviepy.editor import concatenate


image_folder = "images"
songs_folder = "songs"
videos_folder = "videos"
image_duration = 0.8  # Duração de cada imagem no vídeo (em segundos)
transition_duration = 0.2  # Duração da transição entre as imagens (em segundos)
output_file = "output_video.mp4"  # Nome do arquivo de saída do vídeo
text = "Se vc conhece sua namorad@ qual ela vai gostar??"

def add_text_to_image(image_path, text, number=None, video_size=None):
    image = Image.open(image_path)
    
    if video_size:
        video_width = video_size[0]
        image_width, image_height = image.size
        aspect_ratio = image_width / image_height
        new_width = video_width
        new_height = int(new_width / aspect_ratio)
        image = image.resize((new_width, new_height))    
        draw = ImageDraw.Draw(image)

    draw.text((100, 100), f"#{number+1}", font=ImageFont.truetype("./font/Roboto_Mono/static/RobotoMono-Bold.ttf", 100), fill=(0, 0, 0), fontcolor=(255, 255, 255))
    return image

def add_text_to_video(video_clip, text, duration):
    font_path = "./font/Roboto_Mono/static/RobotoMono-Bold.ttf"
    fontsize = 90  # Tamanho inicial da fonte

    text_clip = TextClip(text, fontsize=fontsize, color='white', font=font_path, method='caption', align='center')
    text_clip = text_clip.set_duration(duration)
    text_clip = text_clip.set_position(("center"))
    video_with_text = CompositeVideoClip([video_clip, text_clip])
    return video_with_text


def create_video(text, input_video):
    images = os.listdir(image_folder)
    clips = []

    video_clip = VideoFileClip(input_video)
    video_size = video_clip.size
    start_time = 0  # Tempo de início em segundos
    end_time = 5  # Tempo de término em segundos
    trimmed_clip = video_clip.subclip(start_time, end_time)

    video_with_text = add_text_to_video(trimmed_clip, text, end_time - start_time)
    clips.append(video_with_text)

    for i, image_name in enumerate(images):
        image_path = os.path.join(image_folder, image_name)
        text = f"#{i}"
        image_with_text, image_size = add_text_to_image(image_path, text, number=i, video_size=video_size)
        image_array = np.array(image_with_text) 
        image_clip = ImageClip(image_array).set_duration(image_duration)
        if i < len(images) - 1:
            transition_clip = ImageClip(image_array).set_duration(transition_duration)
            clips.append(transition_clip)
        clips.append(image_clip)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.fps = 24  # Definir o FPS do clipe final (altere o valor se necessário)

    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

def add_audio_to_video():
    audio_path = "music.mp3"
    audio_start_time = 12  # Tempo de início do áudio em segundos
    video_duration = 10  # Duração desejada do vídeo em segundos

    video_clip = VideoFileClip("video_carrossel.mp4")
    audio_clip = AudioFileClip(audio_path)

    # Ajustar a duração do vídeo
    video_clip = video_clip.subclip(0, video_duration)

    # Cortar o áudio para a duração desejada
    audio_clip = audio_clip.subclip(audio_start_time, audio_start_time + video_duration)

    # Definir o áudio no objeto video_clip
    video_with_audio = video_clip.set_audio(audio_clip)
    name = text.replace(" ", "-")

    output_file_with_audio = f"../../../videos/{name}.mp4"
    video_with_audio.write_videofile(output_file_with_audio, codec="libx264", audio_codec="aac")


def delete_medias():
        # Obtém a lista de arquivos na pasta
    arquivos = os.listdir('images')
    
    for arquivo in arquivos:
        # Verifica se o arquivo é uma imagem (pode ajustar os tipos de imagem conforme necessário)
        if arquivo.endswith(".jpg") or arquivo.endswith(".png"):
            # Cria o caminho completo do arquivo
            caminho_arquivo = os.path.join('images', arquivo)
            
            # Deleta o arquivo
            os.remove(caminho_arquivo)
            print(f"Arquivo {arquivo} deletado com sucesso.")

    caminho_video = os.path.join(os.getcwd(), 'video_carrossel.mp4')
    
    # Verifica se o arquivo existe
    if os.path.exists(caminho_video):
        # Deleta o arquivo
        os.remove(caminho_video)
        print(f"Vídeo {'video_carrossel.mp4'} deletado com sucesso.")
    else:
        print(f"O vídeo {'video_carrossel.mp4'} não existe.")


def initial():
    create_video()
    add_audio_to_video()
    # delete_medias()

if __name__ == "__main__":
    initial()
