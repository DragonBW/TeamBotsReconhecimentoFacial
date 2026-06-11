# TeamBotsReconhecimentoFacial
Programa de reconhecimento facial desenvolvido para a TeamBots Uniube.

Clone o repositorio e instale os requerimentos:

```bash
pip install -r requirement.txt
```

Antes de executar o `Reconhecimento.py`, execute o `ChecarBanco.py` para criar o arquivo `.pkl` e verificar se as imagens são válidas.

`Reconhecimento.py`:
Gera uma stream que reconhece indivíduos no banco de dados e identifica rostos desconhecidos. Caso a pessoa seja validada, um trigger é ativado, abrindo a porta por 5 segundos.

`ChecarBanco.py`:
Deve ser utilizado para gerar o arquivo `.pkl` ou quando ele precisar ser atualizado (quando as imagens do banco forem modificadas). Também verifica se todas as imagens são válidas.

`Database`:
Pasta onde as imagens são buscadas. Podem ser utilizadas tanto múltiplas imagens quanto imagens individuais.

  ```bash
  database
 ├── Alice
 │   ├── Alice1.jpg
 │   ├── Alice2.jpg
 ├── Bob
 │   ├── Bob1.jpg
  ```
