import requests
import os
from lxml import etree
from datetime import datetime
from deep_translator import GoogleTranslator
import time

# URL da API JSRDN
url = "https://tv.jsrdn.com/epg/query.php?range=now,2h&id=45144,139216,145581,145582,83822,119200,145127,145591,138029,140186,136898,140613,140616,140614,140615,114364,126120,92945,95229,138031,138032,138214,138215,145579,145580,145589,145586,145587,145588,145583,145584,145500,145504,145506,145416,145415,145126,145128,144990,144993,144994"

headers = {'User-Agent': 'Mozilla/5.0'}
translator = GoogleTranslator(source='auto', target='pt')

# Configuração de Pasta e Arquivo
FOLDER_NAME = "epg"
FILE_NAME = "epg_distrotv.xml"
FILE_PATH = os.path.join(FOLDER_NAME, FILE_NAME)

def format_xmltv_date(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y%m%d%H%M%S +0000')
    except:
        return ""

def translate_description(text):
    if not text or len(text) < 3:
        return text
    try:
        return translator.translate(text)
    except Exception:
        return text

def generate_xmltv():
    try:
        # 1. Cria a pasta 'epg' se ela não existir
        if not os.path.exists(FOLDER_NAME):
            os.makedirs(FOLDER_NAME)
            print(f"Pasta '{FOLDER_NAME}' criada.")

        print("Obtendo dados da JSRDN...")
        response = requests.get(url, headers=headers)
        data = response.json()
        epg_data = data.get('epg', {})
        
        root = etree.Element("tv", generator_info_name="JSRDN_PT_DistroTV")

        for cid, info in epg_data.items():
            # Canal
            channel_name = info.get('title', f"Canal {cid}")
            chan_tag = etree.SubElement(root, "channel", id=str(cid))
            etree.SubElement(chan_tag, "display-name").text = channel_name

            slots = info.get('slots', [])
            for s in slots:
                start = s.get('start')
                end = s.get('end')
                if not start or not end: continue

                prog_tag = etree.SubElement(root, "programme", {
                    "start": format_xmltv_date(start),
                    "stop": format_xmltv_date(end),
                    "channel": str(cid)
                })

                # Título
                title = s.get('title', 'Sem Título')
                etree.SubElement(prog_tag, "title", lang="pt").text = str(title)
                
                # Descrição Traduzida
                desc_original = s.get('description')
                if desc_original:
                    print(f"Traduzindo: {title[:30]}...")
                    desc_pt = translate_description(desc_original)
                    etree.SubElement(prog_tag, "desc", lang="pt").text = str(desc_pt)
                    time.sleep(0.2)

        # 2. Salva o arquivo no caminho específico: epg/epg_distrotv.xml
        xml_output = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        with open(FILE_PATH, "wb") as f:
            f.write(xml_output)
        
        print(f"Sucesso! Arquivo salvo em: {FILE_PATH}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_xmltv()
        
