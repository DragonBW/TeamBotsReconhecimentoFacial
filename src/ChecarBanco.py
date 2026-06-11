from deepface import DeepFace

# Cria ou atualiza o arquivo .pkl do banco de dados e verifica se as imagens são validas.
df = DeepFace.find(img_path="Imagens/target.jpg", db_path="Database")
