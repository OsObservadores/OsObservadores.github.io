# Monitoramento de Posição com Envio de Mensagem no Telegram

Este projeto, localizado em `OsObservadores.github.io/Teste projeto/`, usa OpenCV e MediaPipe para detectar a posição de uma pessoa em frente à webcam. Quando a pessoa fica "em pé" por 5 segundos ou ninguém está detectado por 5 segundos, uma mensagem é enviada via Telegram.

## Requisitos

- Python 3.7+
- Webcam conectada
- Bot do Telegram criado com token e chat ID configurados
- Um tabuleiro em uma folha A4 de 7x9 quadrados, para calibração da câmera

## Como usar

1. Navegue até o diretório do projeto:

```bash
cd "OsObservadores.github.io/Teste projeto/"
```

  Crie um arquivo .env na raiz desse diretório com as variáveis:
```
TELEGRAM_TOKEN=seu_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
```
## Tutorial para obter Token e Chat ID no Telegram

[![Assistir vídeo explicativo](https://img.youtube.com/vi/l5YDtSLGhqk/0.jpg)](https://www.youtube.com/watch?v=l5YDtSLGhqk)


  Instale as dependências:
```
pip install -r requirements.txt
```

## Calibração de câmera

   Execute o script "capture.py" para tirar fotos do tabuleiro:
```
python capture.py
```
   1. Enquanto o script esta rodando, segure o tabuleiro em frente a câmera de forma que todos os quadrados do tabuleiro estejam visiveis na tela e sem reflexo.
   2. Tire no mínimo 15 fotos do tabuleiro apertando a tecla "s" do teclado, em posições diferentes mas respeitando a regra 1.
   3. Após as 15 fotos, aperte a tecla "q" do teclado para sair

  Com isso, já é possível calibrar a câmera usando um padrão confiavel.
  
  Para realizar a calibração a partir das fotos, execute o script "calibration.py"
```
python calibration.py
```

  Agora que a câmera está calibrada, já é possível usar o script principal "posevideo.py"
```
python posevideo.py
```
## Resultados Esperados
Notificação no telegram:
- Após 5 segundos com a pessoa filmada ser identificada **estando de pé**.
- Após 5 segundos com a pessoa filmada não ser identificada pela câmera, estando assim **ausente**.
## Observações

  Pressione q para sair da aplicação.

  O chat ID pode ser de um grupo ou conversa individual.

## Licença

Este projeto é open source.
