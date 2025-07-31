# Monitoramento de Posição com Envio de Mensagem no Telegram

Este projeto, localizado em `OsObservadores.github.io/Teste projeto/`, usa OpenCV e MediaPipe para detectar a posição de uma pessoa em frente à webcam. Quando a pessoa fica "em pé" por 5 segundos ou ninguém está detectado por 5 segundos, uma mensagem é enviada via Telegram.

## Requisitos

- Python 3.7+
- Webcam conectada
- Bot do Telegram criado com token e chat ID configurados

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
  Tutorial para obter Token e Chat ID no Telegram

Veja o vídeo explicativo abaixo:

<iframe width="560" height="315" src="https://www.youtube.com/embed/l5YDtSLGhqk" title="YouTube video player" frameborder="0" allowfullscreen></iframe>

  Instale as dependências:
```
pip install -r requirements.txt
```
   Execute o script principal (ajuste o nome do script se for diferente):
```
python seu_script.py
```
## Observações

  Pressione q para sair da aplicação.

  O chat ID pode ser de um grupo ou conversa individual.

## Licença

Este projeto é open source.
