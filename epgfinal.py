import requests
import gzip
from lxml import etree
import os

# Configurações
EPG_SOURCES = [
    "https://x1co.com.br/epg/epg.xml",
    "https://raw.githubusercontent.com/JulioCesarXY/gratis/refs/heads/main/epg/epg_kpoptvbr.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml"
]

OUTPUT_DIR = "epg"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "epg_final.xml")

def fetch_content(url):
    print(f"Baixando: {url}")
    try:
        # User-agent para evitar bloqueios de alguns servidores
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        
        if url.endswith(".gz") or response.content.startswith(b'\x1f\x8b'):
            return gzip.decompress(response.content)
        return response.content
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return None

def merge_epgs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    combined_root = etree.Element("tv")
    combined_root.set("generator-info-name", "EPG-Merger-Pro")

    # Conjunto para rastrear IDs de canais já adicionados e evitar duplicatas
    added_channels = set()

    for url in EPG_SOURCES:
        content = fetch_content(url)
        if content:
            try:
                parser = etree.XMLParser(recover=True, remove_blank_text=True)
                tree = etree.fromstring(content, parser=parser)
                
                # 1. Processar Canais
                for channel in tree.xpath("//channel"):
                    channel_id = channel.get("id")
                    if channel_id not in added_channels:
                        combined_root.append(channel)
                        added_channels.add(channel_id)
                
                # 2. Processar Programação
                for programme in tree.xpath("//programme"):
                    combined_root.append(programme)
                
                print(f"Dados integrados com sucesso: {url}")
            except Exception as e:
                print(f"Erro ao processar XML de {url}: {e}")

    # Salva o arquivo final com indentação correta
    final_tree = etree.ElementTree(combined_root)
    final_tree.write(
        OUTPUT_FILE, 
        encoding="utf-8", 
        xml_declaration=True, 
        pretty_print=True
    )
    print(f"\nConcluído! Total de canais únicos: {len(added_channels)}")
    print(f"Arquivo salvo em: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_epgs()
