import os
from datetime import datetime, timedelta

def gerar_xml_epg():
    channel_id = "KpopTV.br"
    channel_name = "KpopTV.br"
    # Pega a data atual
    data_base = datetime.now()
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<tv generator-info-name="GeminiEPG-Automated">',
        f'  <channel id="{channel_id}">',
        f'    <display-name lang="pt">{channel_name}</display-name>',
        '    <icon src="https://link-da-logo.com/kpoptvbr.png" />',
        '  </channel>'
    ]

    # Gera para os próximos 7 dias
    for i in range(8):
        dia_atual = data_base + timedelta(days=i)
        amanha = dia_atual + timedelta(days=1)
        
        str_hoje = dia_atual.strftime("%Y%m%d")
        str_amanha = amanha.strftime("%Y%m%d")
        dia_semana = dia_atual.weekday() # 0=Segunda, 2=Quarta, 4=Sexta

        # --- Definição dos Blocos Horários ---
        
        # 01h00 às 18h00 - Programação Musical
        xml_lines.append(f'  <programme start="{str_hoje}010000 -0300" stop="{str_hoje}180000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">Programação Musical</title>')
        xml_lines.append('    <desc lang="pt">Sua trilha sonora de K-Pop para o dia todo.</desc>')
        xml_lines.append('  </programme>')

        # 18h00 às 19h00 - Programação Musical (Preenchimento)
        xml_lines.append(f'  <programme start="{str_hoje}180000 -0300" stop="{str_hoje}190000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">Programação Musical</title>')
        xml_lines.append('    <desc lang="pt">Aquecimento para os hits da noite.</desc>')
        xml_lines.append('  </programme>')

        # 19h00 - Hits On Top
        xml_lines.append(f'  <programme start="{str_hoje}190000 -0300" stop="{str_hoje}200000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">Hits On Top</title>')
        xml_lines.append('    <desc lang="pt">Os clipes mais quentes do momento.</desc>')
        xml_lines.append('  </programme>')

        # 20h00 - Boys vs Girls
        xml_lines.append(f'  <programme start="{str_hoje}200000 -0300" stop="{str_hoje}210000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">Boys vs Girls</title>')
        xml_lines.append('    <desc lang="pt">A disputa entre os melhores grupos masculinos e femininos.</desc>')
        xml_lines.append('  </programme>')

        # 21h00 - MV e Letra
        xml_lines.append(f'  <programme start="{str_hoje}210000 -0300" stop="{str_hoje}213000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">MV e Letra</title>')
        xml_lines.append('    <desc lang="pt">Aprenda a letra enquanto assiste ao MV.</desc>')
        xml_lines.append('  </programme>')

        # 21h30 - Dança e Joga (Seg/Qua/Sex) ou Programação Musical
        if dia_semana in [0, 2, 4]:
            titulo, desc = "Dança e Joga", "Coreografias e games interativos."
        else:
            titulo, desc = "Programação Musical", "A melhor seleção de clipes."

        xml_lines.append(f'  <programme start="{str_hoje}213000 -0300" stop="{str_hoje}214500 -0300" channel="{channel_id}">')
        xml_lines.append(f'    <title lang="pt">{titulo}</title>')
        xml_lines.append(f'    <desc lang="pt">{desc}</desc>')
        xml_lines.append('  </programme>')

        # 21h45 - Programação Musical
        xml_lines.append(f'  <programme start="{str_hoje}214500 -0300" stop="{str_hoje}233000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">Programação Musical</title>')
        xml_lines.append('    <desc lang="pt">Clipes variados para fechar a noite.</desc>')
        xml_lines.append('  </programme>')

        # 23h30 - Old K-Pop (vai até 01h00 do dia seguinte)
        xml_lines.append(f'  <programme start="{str_hoje}233000 -0300" stop="{str_amanha}010000 -0300" channel="{channel_id}">')
        xml_lines.append('    <title lang="pt">Old K-Pop</title>')
        xml_lines.append('    <desc lang="pt">Os clássicos que fizeram história.</desc>')
        xml_lines.append('  </programme>')

    xml_lines.append('</tv>')

    # Salva o arquivo
    with open("epg_kpoptvbr.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines))
    
    print("EPG gerado com sucesso!")

if __name__ == "__main__":
    gerar_xml_epg()
