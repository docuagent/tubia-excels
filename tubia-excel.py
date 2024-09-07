import pandas as pd
import os
import numpy as np
import re

mov_bancarios = pd.read_excel(path + 'Movimientos de cuenta - GALICIA.xlsx')
comp_emitidos = pd.read_excel(path + 'Comprobantes Emitidos - AFIP.xlsx', header = 1)
comp_recibidos = pd.read_excel(path + 'Comprobantes Recibidos - AFIP.xlsx', header = 1)

#Movimientos bancarios
mov_bancarios['Importe'] = mov_bancarios['Créditos'] - mov_bancarios['Débitos']
mov_bancarios['Tipo_comprobante'] = ""
mov_bancarios.rename(columns = {"Grupo de Conceptos" : "Grupo_conceptos", "Leyendas Adicionales 2" : "Cuit"}, inplace = True)
mov_bancarios = mov_bancarios[["Fecha", "Importe", "Grupo_conceptos", "Concepto", "Cuit", "Tipo_comprobante"]]
#Modificamos la fecha
mov_bancarios['Fecha'] = pd.to_datetime(mov_bancarios['Fecha'], dayfirst=True).dt.strftime('%Y-%m-%d')
# Algunos campos no son CUITS, esos los sacamos
regex = r'^(20|23|24|27|30|33|34)-?\d{8}-?\d$'
mov_bancarios['Cuit'] = mov_bancarios['Cuit'].apply(lambda x: "" if pd.isna(x) else (x if re.match(regex, str(x)) else ""))

#Comprobantes emitidos
comp_emitidos['Grupo_conceptos'] = "Comprobantes"
comp_emitidos['Concepto'] = "Comprobante emitido"
comp_emitidos.rename(columns = {"Nro. Doc. Receptor" : "Cuit", "Imp. Total" : "Importe", "Tipo" : "Tipo_comprobante"}, inplace = True)
comp_emitidos['Importe'] = comp_emitidos['Importe'] * -1
comp_emitidos = comp_emitidos[["Fecha", "Importe", "Grupo_conceptos", "Concepto", "Cuit", "Tipo_comprobante"]]
#Modificamos la fecha
comp_emitidos['Fecha'] = pd.to_datetime(comp_emitidos['Fecha'], dayfirst=True).dt.strftime('%Y-%m-%d')

#Comprobantes recibidos
comp_recibidos['Grupo_conceptos'] = "Comprobantes"
comp_recibidos['Concepto'] = "Comprobante recibido"
comp_recibidos.rename(columns = {"Nro. Doc. Emisor" : "Cuit", "Imp. Total" : "Importe", "Tipo" : "Tipo_comprobante"}, inplace = True)
comp_recibidos = comp_recibidos[["Fecha", "Importe", "Grupo_conceptos", "Concepto", "Cuit", "Tipo_comprobante"]]
#Modificamos la fecha
comp_recibidos['Fecha'] = pd.to_datetime(comp_recibidos['Fecha'], dayfirst=True).dt.strftime('%Y-%m-%d')

#Dataset final
df_final = pd.concat([mov_bancarios, comp_emitidos, comp_recibidos])
df_final['Cuit'] = df_final['Cuit'].astype(str)

df_final.to_excel(path + 'movimientos_final_test.xlsx', index = False)