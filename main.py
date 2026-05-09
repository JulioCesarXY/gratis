import requests
from lxml import etree
from datetime import datetime
import os

url = "https://tv.jsrdn.com/epg/query.php?range=now,2h&id=45144,139216,145581,145582,83822,119200,145127,145591,138029,140186,136898,140613,140616,140614,140615,114364,126120,92945,95229,138031,138032,138214,138215,145579,145580,145589,145586,145587,145588,145583,145584,145500,145504,145506,145416,145415,145126,145128,144990,144993,144994"

headers = {'User-Agent': 'Mozilla/5.0'}

def format_xmltv_date(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y%m%d%H%M%S +0000')
    except:
        return ""

def generate_xmltv():
    try:
        # Cria a pasta epg se não existir
        if not os.path.exists('epg'):
            os.makedirs('epg')

        print("Lendo dados da JSRDN...")
        response = requests.get(url, headers=headers)
        data = response.json()
        epg_data = data.get('epg', {})
        
        root = etree.Element("tv", generator_info_name="JSRDN_Automation")

        for cid, info in epg_data.items():
            channel_name = info.get('title', f"Channel {cid}")
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

                title = s.get('title', 'No Title')
                etree.SubElement(prog_tag, "title", lang="en").text = str(title)
                
                desc = s.get('description')
                if desc:
                    etree.SubElement(prog_tag, "desc", lang="en").text = str(desc)

        # Caminho atualizado conforme seu pedido
        save_path = os.path.join('epg', 'epg_distrotv.xml')
        xml_output = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        
        with open(save_path, "wb") as f:
            f.write(xml_output)
        
        print(f"Sucesso! Salvo em {save_path}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    generate_xmltv()
