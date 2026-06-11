import threading
from deepface import DeepFace
import cv2
import time

cap =cv2.VideoCapture(0)

contador = 0
trava = threading.Lock()
identidade = "Inicializando..."
caixa = None
autorizado = False
timer_inicio = None

caixa_atual = None
SUAVIZACAO = 0.2

# Função para checar a identidade.
def Checar(frame):
    global identidade, caixa, autorizado, timer_inicio

    try:
        # Busca no banco as imagens com maior confiança.
        resultados = DeepFace.find(frame, db_path="Database", enforce_detection=False, silent=True)

        texto = "Sem rosto"
        caixa_temp = None

        # Verifica se o resultado é uma lista e se contém dados.
        if isinstance(resultados, list) and len(resultados) > 0:
            df = resultados[0]

        # Para verificar confiança e a identidade, pode ser removido.
        print(df)

        # Verifica se o DataFrame não está vazio e se a confiança é alta.
        if not df.empty and "identity" in df.columns and df.iloc[0]['confidence'] > 60.0:
            # Busca o nome do indivíduo a partir do caminho da pasta.
            identidade_caminho = df.iloc[0]['identity']
            nome = identidade_caminho.split('/')[-2] if '/' in identidade_caminho else identidade_caminho.split('\\')[-2]
            texto = f"identidade: {nome}"

            #autoriza a abertura da porta e inicia um timer de 5 segundos.
            autorizado = True
            timer_inicio = time.perf_counter()

            # Extrai as coordenadas do rosto.
            x = int(df.iloc[0]["source_x"])
            y = int(df.iloc[0]["source_y"])
            w = int(df.iloc[0]["source_w"])
            h = int(df.iloc[0]["source_h"])
            caixa_temp = (x, y, w, h)
        else:
            # Se o rosto não for reconhecido, tenta extrair as coordenadas.
            try:
                rosto = DeepFace.extract_faces(img_path=frame, enforce_detection=True)
                if rosto:
                    texto = "Desconhecido"
                    area = rosto[0]["facial_area"]
                    caixa_temp = (area["x"], area["y"], area["w"], area["h"])
            except Exception:
                pass
    except Exception as e:
        texto = "Erro no processamento"
        caixa_temp = None

    with trava:
        identidade = texto
        caixa = caixa_temp

if not cap.isOpened():
    print("Não foi possível acessar a câmera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível ler o quadro da câmera.")
        break



    # Realiza a verificação de imagem a cada 30 quadros.
    if contador % 30 == 0:
        threading.Thread(target=Checar, args=(frame.copy(),)).start()
    contador += 1

    with trava:
        #timer de 5 segundos para autorização da porta.
        timer_fim = time.perf_counter()
        if timer_inicio is not None and timer_fim >= timer_inicio + 5:
            autorizado = False
            timer_inicio = None

        # Suaviza o movimento da caixa através de interpolação.
        if caixa is not None:
            if caixa_atual is None:
                caixa_atual = list(caixa)
            else:
                for i in range(4):
                    caixa_atual[i] += (caixa[i] - caixa_atual[i]) * SUAVIZACAO
        else:
            caixa_atual = None

        # Renderiza a caixa ao redor do rosto.
        if caixa_atual is not None:
            x, y, w, h = map(int, caixa_atual)
            cor_caixa = (0, 255, 0) if "identidade" in identidade else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), cor_caixa, 2)

        # Renderiza o texto de identidade e o status da porta.
        cor_texto = (0,255,0) if "identidade" in identidade else (0,0,255)
        cv2.putText(frame, identidade, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, cor_texto, 2, cv2.LINE_AA)
        cv2.putText(frame, "Porta Destravada", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA) if autorizado else cv2.putText(frame, "Porta Travada", (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    #mostra o vídeo na tela.
    cv2.imshow('Reconhecimento Facial', frame)

    # Encerra o programa com a tecla 'q'.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break