# 📺 Playlist Multi-Idiomas & EPG Automatizado

Bem-vindo ao repositório! Este projeto oferece uma curadoria organizada de canais gratuitos e webcanais de diversos países, categorizados para facilitar a sua navegação. Além da lista, contamos com um sistema de automação que garante a atualização constante do Guia de Programação (EPG).

---

## 🚀 Destaques do Projeto

*   **Organização por Idiomas:** Conteúdo em Português, Inglês, Espanhol e mais.
*   **Categorização Inteligente:** Canais divididos por gêneros como Notícias, Esportes, Entretenimento, Documentários, Músicas e Infantil.
*   **EPG Sempre Atual:** Automação via GitHub Actions que gera e atualiza o arquivo XMLTV periodicamente.
*   **Compatibilidade:** Funciona em qualquer player que suporte listas M3U8 (IPTV Smarters, TiviMate, VLC, OTT Navigator, etc).

---

## 🛠️ Como utilizar

Para utilizar no seu player favorito, basta copiar o link abaixo e colar na configuração de "Lista de Reprodução":

> **URL da Playlist:** `https://raw.githubusercontent.com/JulioCesarXY/gratis/main/iptvrevisado.m3u`

Para configurar o Guia de Programação (EPG):

> **URL do EPG:** `https://raw.githubusercontent.com/JulioCesarXY/gratis/main/epg_final.xml`

---

## 📂 Categorias Disponíveis

| Categoria | Descrição |
| :--- | :--- |
| **Geral** | Canais de variedades e entretenimento local. |
| **Notícias** | Cobertura jornalística 24h nacional e internacional. |
| **Músicas** | Músicas dos mais variados gêneros. |
| **Documentários** | Ciência, natureza e história. |
| **Kids** | Desenhos e conteúdos educativos. |
| **Webcanais** | Transmissões exclusivas da internet e lives 24/7. |

---

## 🤖 Automação do EPG

O diferencial deste repositório é o script de automação integrado. 

1.  **Sincronização:** O script faz o scraping/coleta das grades de programação diretamente das fontes oficiais.
2.  **Processamento:** Os dados são limpos e formatados no padrão XMLTV.
3.  **Deploy:** O arquivo `epg_final.xml` é atualizado automaticamente todos os dias às **00:00 UTC** através do GitHub Actions.

---

## 🤝 Contribuição

Encontrou um link offline ou tem uma sugestão de canal?
1. Abra uma **Issue** relatando o problema.
2. Envie um **Pull Request** com a correção ou adição.

---

## ⚖️ Isenção de Responsabilidade (Disclaimer)

Este repositório **não hospeda** nenhum arquivo de vídeo ou streaming. Apenas agrupamos links que já estão disponíveis publicamente na internet e em plataformas de distribuição gratuita. Todos os direitos pertencem aos seus respectivos proprietários.

---
*Desenvolvido com ❤️ para a comunidade.*
