import requests
import gzip
import shutil
from lxml import etree
import os

# Configurações
EPG_SOURCES = [
    "https://x1co.com.br/epg/epg.xml",
    "https://raw.githubusercontent.com/JulioCesarXY/gratis/refs/heads/main/epg/epg_kpoptvbr.xml",
    "https://raw.githubusercontent.com/BuddyChewChew/localnow-playlist-generator/refs/heads/main/epg.xml",
    "https://epgshare01.online/epgshare01/epg_ripper_DUMMY_CHANNELS.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PLEX1.xml.gz",
    "https://raw.githubusercontent.com/JulioCesarXY/gratis/refs/heads/main/epg/epg_distrotv.xml"
]

OUTPUT_DIR = "epg"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "epg_final.xml")
OUTPUT_FILE_GZ = os.path.join(OUTPUT_DIR, "epg_final.xml.gz") # Novo caminho do arquivo .gz

def fetch_content(url):
    print(f"Baixando: {url}")
    try:
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

    added_channels = set()

    for url in EPG_SOURCES:
        content = fetch_content(url)
        if content:
            try:
                parser = etree.XMLParser(recover=True, remove_blank_text=True)
                tree = etree.fromstring(content, parser=parser)
                
                for channel in tree.xpath("//channel"):
                    channel_id = channel.get("id")
                    if channel_id not in added_channels:
                        combined_root.append(channel)
                        added_channels.add(channel_id)
                
                for programme in tree.xpath("//programme"):
                    combined_root.append(programme)
                
                print(f"Dados integrados com sucesso: {url}")
            except Exception as e:
                print(f"Erro ao processar XML de {url}: {e}")

    # 1. Salva o arquivo XML normal
    final_tree = etree.ElementTree(combined_root)
    final_tree.write(
        OUTPUT_FILE, 
        encoding="utf-8", 
        xml_declaration=True, 
        pretty_print=True
    )

    # 2. Salva o arquivo em formato .gz (Comprimido)
    try:
        with open(OUTPUT_FILE, 'rb') as f_in:
            with gzip.open(OUTPUT_FILE_GZ, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Arquivo comprimido salvo em: {OUTPUT_FILE_GZ}")
    except Exception as e:
        print(f"Erro ao criar arquivo GZ: {e}")

    print(f"\nConcluído! Total de canais únicos: {len(added_channels)}")
    print(f"Arquivo XML salvo em: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_epgs()
    
