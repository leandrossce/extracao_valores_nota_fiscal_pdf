import fitz  # PyMuPDF
import re
import os

def extrair_valor_numerico(texto):
    # Procura por padrões numéricos no texto, por exemplo, valores monetários ou números
    # Esta expressão regular procura por números que possam ter pontos como separadores de milhares
    # e vírgula para a parte decimal, como comum em formatos brasileiros.
    padrao_numerico = re.compile(r'\b\d{1,3}(?:\.\d{3})*(?:,\d+)?\b')
    resultado = padrao_numerico.findall(texto)
    # Retornar apenas o primeiro valor encontrado ou None se nenhum valor for encontrado
    return resultado[0] if resultado else None


def encontrar_coordenadas_rotulo(pdf_path, rotulo):
    # Abre o documento PDF
    doc = fitz.open(pdf_path)
    # Itera sobre cada página do documento
    for num_pagina, pagina in enumerate(doc):
        # Procura pelo rótulo em cada página
        texto_instancias = pagina.search_for(rotulo)
        for inst in texto_instancias:
            # Retorna as coordenadas da primeira instância do rótulo encontrado
            return num_pagina, inst
    return None, None

def extrair_texto_area(pdf_path, rotulo, delta_x0, delta_y0, delta_x1, delta_y1):
    num_pagina, coordenadas_rotulo = encontrar_coordenadas_rotulo(pdf_path, rotulo)
    if coordenadas_rotulo:
        doc = fitz.open(pdf_path)
        pagina = doc[num_pagina]
        area_interesse = ajustar_area_interesse(coordenadas_rotulo, delta_x0, delta_y0, delta_x1, delta_y1)
        # Extrai o texto da área de interesse
        texto = pagina.get_text("text", clip=area_interesse)
        return texto
    else:
        print("Rótulo não encontrado.")
        return ""

valores_notas_fiscais=[]

def processar_pdf(diretorio, rotulo, delta_x0, delta_y0, delta_x1, delta_y1):
    # Lista todos os arquivos no diretório
    for filename in os.listdir(diretorio):
        if filename.endswith('.pdf'):
            # Caminho completo para o arquivo PDF
            pdf_path = os.path.join(diretorio, filename)

            # Determina a página que contém o rótulo e as coordenadas do rótulo
            num_pagina, coordenadas_rotulo = encontrar_coordenadas_rotulo(pdf_path, rotulo)

            # Abre o documento PDF
            doc = fitz.open(pdf_path)
            # Itera sobre cada página do documento
            if coordenadas_rotulo:
                doc = fitz.open(pdf_path)
                pagina = doc[num_pagina]
                area_interesse = ajustar_area_interesse(coordenadas_rotulo, delta_x0, delta_y0, delta_x1, delta_y1)
                # Extrai o texto da área de interesse
                texto = pagina.get_text("text", clip=area_interesse)

                valor_numerico  = extrair_valor_numerico(texto) # Extrair apenas valor numérico
                valor_numerico_float = converter_para_float(valor_numerico) # Converter para Float
                if valor_numerico_float is  None:
                    valor_numerico_float=0

                valores_notas_fiscais.append(valor_numerico_float) #adiciona valor encontraro na lista

            else:
                print("Rótulo não encontrado.")
           
            doc.close()

def ajustar_area_interesse(coordenadas_rotulo, delta_x0, delta_y0, delta_x1, delta_y1):
    # Ajusta as coordenadas para a área de interesse
    area_interesse = fitz.Rect(
        coordenadas_rotulo.x0 + delta_x0,
        coordenadas_rotulo.y1 + delta_y0,  # Começar no y1 do rótulo para ir abaixo
        coordenadas_rotulo.x1 + delta_x1,
        coordenadas_rotulo.y1 + delta_y1   # Extender abaixo do y1 do rótulo
    )
    return area_interesse

def converter_para_float(valor_numerico):
    if valor_numerico:
        # Remove os pontos de separação de milhar
        valor_sem_milhar = valor_numerico.replace('.', '')
        # Substitui a vírgula do decimal por ponto
        valor_decimal = valor_sem_milhar.replace(',', '.')
        return float(valor_decimal)
    else:
        return None
    

def extrair_texto_area(pdf_path, rotulo, delta_x0, delta_y0, delta_x1, delta_y1):
    num_pagina, coordenadas_rotulo = encontrar_coordenadas_rotulo(pdf_path, rotulo)
    if coordenadas_rotulo:
        doc = fitz.open(pdf_path)
        pagina = doc[num_pagina]
        area_interesse = ajustar_area_interesse(coordenadas_rotulo, delta_x0, delta_y0, delta_x1, delta_y1)
        # Extrai o texto da área de interesse
        texto = pagina.get_text("text", clip=area_interesse)
        return texto
    else:
        print("Rótulo não encontrado.")
        return ""



# Exemplo de uso:
pdf_path = "C:\\Users\\Gabriel\\Downloads\\esse\\"
rotulo = "TOTAL DA NOTA"
# Os deltas são exemplos e devem ser ajustados conforme a localização do conteúdo desejado
delta_x0 = 0    # Sem deslocamento horizontal inicial
delta_y0 = 5    # Começar um pouco abaixo do final do rótulo
delta_x1 = 100  # Estender a caixa para a direita para cobrir a largura do valor
delta_y1 = 20   # Estender a caixa para baixo para cobrir a altura do valor

'''     # teste para apenas 1 pdf
pdf_path = "C:\\Users\\Gabriel\\Downloads\\esse\\esse.pdf"

texto_area = extrair_texto_area(pdf_path, rotulo, delta_x0, delta_y0, delta_x1, delta_y1)
valor_numerico  = extrair_valor_numerico(texto_area)
valor_numerico_float = converter_para_float(valor_numerico)
if valor_numerico_float is  None:
    valor_numerico_float=0
print(texto_area)
'''

#Vai processar todos os PDF de notas contidos no diretório apontado em pdf_path
processar_pdf(pdf_path,rotulo, delta_x0, delta_y0, delta_x1, delta_y1)

print(valores_notas_fiscais)
