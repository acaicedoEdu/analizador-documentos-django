import os
import csv
import json
from datetime import datetime
from django.conf import settings
from .models import DataImport, COLUMNS_DB

class FileProcessor:
    def __init__(self):
        # Intervalos de columnas
        self.intervals = [
            (0, 10),
            (10, 13),
            (13, 28),
            (28, 128), 
            (128, 143),
            (143, 165), 
            (165, 187),
            (187, 201), 
            (201, 221), 
            (221, 226), 
            (226, 241),
            (241, 256),
            (256, 271), 
            (271, 321),
            (321, 371),
            (371, 494),
            (494, 548),
            (548, 568),
            (568, 575),
            (575, 615), 
            (615, 625),
            (625, 1615)
        ]

    # Extrae las columnas de una línea según los rangos definidos
    def columns_line(self, line):
        columns = []
        for start, end in self.intervals:
            if end <= len(line):
                column_data = line[start:end].strip()
                columns.append(column_data)
            else:
                columns.append('')

        return columns

    # Extrae la fecha del nombre del archivo PRUEBA_20250529.txt
    def archivename_date(self, filename):
        try:
            date_part = filename.split('_')[1].split('.')[0]  # 20250529
            date_obj = datetime.strptime(date_part, '%Y%m%d')
            return date_obj, date_obj.strftime('%m')
        except Exception as e:
            print(f"Error parsing date from filename {filename}: {e}")
            return datetime.now(), datetime.now().strftime('%m')

    # Determina los canales de comunicación disponibles
    def channels_communication(self, column_28):
        channels = {
            'telefono': '1' if 'Línea telefónica' in column_28 else '',
            'whatsapp': '1' if 'whatsapp' in column_28.lower() else '',
            'texto': '1' if 'Mensaje de texto' in column_28 else '',
            'email': '1' if 'Correo electrónico' in column_28 else '',
            'fisica': '1' if 'Correspondencia fisica' in column_28 else ''
        }
        return channels

    # Determina el mejor canal según las reglas de prioridad
    def best_channel(self, channels, telefono_1, telefono_2, telefono_3, correo_electronico):
        priority_order = ['texto', 'email', 'telefono', 'whatsapp', 'fisica']
        
        active_channels = [channel for channel in priority_order if channels[channel] == '1']
        
        if not active_channels:
            mejor_canal = 'texto'
        else:
            mejor_canal = active_channels[0]
        
        contactar_al = ''
        
        if mejor_canal in ['texto', 'telefono', 'whatsapp']:
            if telefono_1.strip():
                contactar_al = telefono_1.strip()
            elif telefono_2.strip():
                contactar_al = telefono_2.strip()
            elif telefono_3.strip():
                contactar_al = telefono_3.strip()
            else:
                if correo_electronico.strip():
                    mejor_canal = 'email'
                    contactar_al = correo_electronico.strip()
                
        elif mejor_canal == 'email':
            if correo_electronico.strip():
                contactar_al = correo_electronico.strip()
            else:
                alt_channels = ['texto', 'telefono', 'whatsapp']
                for alt_channel in alt_channels:
                    if channels[alt_channel] == '1':
                        if telefono_1.strip():
                            mejor_canal = alt_channel
                            contactar_al = telefono_1.strip()
                            break
                        elif telefono_2.strip():
                            mejor_canal = alt_channel
                            contactar_al = telefono_2.strip()
                            break
                        elif telefono_3.strip():
                            mejor_canal = alt_channel
                            contactar_al = telefono_3.strip()
                            break
                
        return mejor_canal, contactar_al

    # Procesa una línea del archivo y retorna un diccionario con los datos
    def process_line(self, line, filename):
        columns = self.columns_line(line)
        
        # Traer fecha del archivo
        fecha_archivo, mes_archivo = self.archivename_date(filename)
        
        # Procesar columna 5 (producto + poliza)
        col5 = columns[4] if len(columns) > 4 else ''
        producto = col5[:5] if len(col5) >= 5 else col5
        poliza = col5[5:] if len(col5) > 5 else ''
        
        # Procesar columna 6 (periodo + valor_asegurado)
        col6 = columns[5] if len(columns) > 5 else ''
        periodo = col6[:1] if col6 else ''
        valor_asegurado = col6[1:] if len(col6) > 1 else ''
        
        # Procesar columna 16 (fecha_venta + fecha_nacimiento + tipo_trans + beneficiarios)
        col16 = columns[15] if len(columns) > 15 else ''
        fecha_venta = col16[:10] if len(col16) >= 10 else ''
        fecha_nacimiento = col16[10:20] if len(col16) >= 20 else ''
        tipo_trans = col16[20:23] if len(col16) >= 23 else ''
        beneficiarios = col16[23:] if len(col16) > 23 else ''
        
        # Procesar columna 17 (genero + sucursal)
        col17 = columns[16] if len(columns) > 16 else ''
        genero = col17[:1] if col17 else ''
        sucursal = col17[1:] if len(col17) > 1 else ''
        
        # Procesar última columna para canales de comunicación
        last_col = columns[-1] if columns else ''
        channels = self.channels_communication(last_col)
        
        # Obtener datos de teléfonos y correo
        telefono_1 = columns[10] if len(columns) > 10 else ''
        telefono_2 = columns[11] if len(columns) > 11 else ''
        telefono_3 = columns[12] if len(columns) > 12 else ''
        correo_electronico = columns[26] if len(columns) > 26 else ''
        
        # Determinar mejor canal
        mejor_canal, contactar_al = self.best_channel(
            channels, telefono_1, telefono_2, telefono_3, correo_electronico
        )
        
        # Construir el registro
        data_line = {
            'tipo_documento': columns[1] if len(columns) > 1 else '',
            'documento': columns[2] if len(columns) > 2 else '',
            'nombre': columns[3] if len(columns) > 3 else '',
            'producto': producto,
            'poliza': poliza,
            'periodo': periodo,
            'valor_asegurado': valor_asegurado,
            'valor_prima': columns[6] if len(columns) > 6 else '',
            'doc_cobro': columns[7] if len(columns) > 7 else '',
            'fecha_ini': columns[8] if len(columns) > 8 else '',
            'fecha_fin': '',
            'dias': columns[9] if len(columns) > 9 else '',
            'telefono_1': telefono_1,
            'telefono_2': telefono_2,
            'telefono_3': telefono_3,
            'ciudad': columns[13] if len(columns) > 13 else '',
            'departamento': columns[14] if len(columns) > 14 else '',
            'fecha_venta': fecha_venta,
            'fecha_nacimiento': fecha_nacimiento,
            'tipo_trans': tipo_trans,
            'beneficiarios': beneficiarios,
            'genero': genero,
            'sucursal': sucursal,
            'tipo_cuenta': '',
            'ultimos_digitos_cuenta': columns[17] if len(columns) > 17 else '',
            'entidad_bancaria': columns[18] if len(columns) > 18 else '',
            'nombre_banco': columns[19] if len(columns) > 19 else '',
            'estado_debito': columns[20] if len(columns) > 20 else '',
            'causal_rechazo': columns[21] if len(columns) > 21 else '',
            'codigo_canal': columns[22][:3] if len(columns) > 22 and len(columns[22]) >= 3 else '',
            'descripcion_canal': columns[23] if len(columns) > 23 else '',
            'codigo_estrategia': columns[24] if len(columns) > 24 else '',
            'tipo_estrategia': columns[25] if len(columns) > 25 else '',
            'correo_electronico': correo_electronico,
            'fecha_entrega_colmena': fecha_archivo.strftime('%Y-%m-%d'),
            'mes_a_trabajar': mes_archivo,
            'id': '',
            'nombre_db': filename,
            'telefono': channels['telefono'],
            'whatsapp': channels['whatsapp'],
            'texto': channels['texto'],
            'email': channels['email'],
            'fisica': channels['fisica'],
            'mejor_canal': mejor_canal,
            'contactar_al': contactar_al
        }
        
        return data_line

    # Funcion que procesa el archivo
    def process_archive(self, archive_path):
        archivename = os.path.basename(archive_path)
        data_json = []
        
        try:
            with open(archive_path, 'r', encoding='utf-8') as archive:
                for line_num, line in enumerate(archive, 1):
                    if line.strip():  # Validacion para líneas vacías
                        try:
                            data_line = self.process_line(line, archivename)
                            data_json.append(data_line)
                        except Exception as e:
                            print(f"Error procesando línea {line_num}: {e}")
                            continue
            
            return data_json
            
        except Exception as e:
            print(f"Error leyendo archivo {archive_path}: {e}")
            return []

    # Funcion que guarda los registros en un archivo CSV
    def save_csv(self, data_json, output_path):
        if not data_json:
            return False
            
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=COLUMNS_DB)
                writer.writeheader()
                writer.writerows(data_json)
            return True
        except Exception as e:
            print(f"Error guardando CSV: {e}")
            return False

    # Funcion que guarda los registros en la base de datos
    def save_db(self, data_json):
        saved_count = 0
        errors = []
        
        for data_line in data_json:
            try:

                if data_line['fecha_ini']:
                    try:
                        fecha_ini = datetime.strptime(data_line['fecha_ini'], '%Y-%m-%d').date()
                    except:
                        fecha_ini = datetime.now().date()
                else:
                    fecha_ini = datetime.now().date()
                
                fecha_entrega_colmena = datetime.strptime(data_line['fecha_entrega_colmena'], '%Y-%m-%d').date()
                
                data_import = DataImport(
                    tipo_documento=data_line['tipo_documento'],
                    documento=data_line['documento'],
                    nombre=data_line['nombre'],
                    producto=data_line['producto'],
                    poliza=data_line['poliza'],
                    periodo=data_line['periodo'],
                    valor_asegurado=data_line['valor_asegurado'],
                    valor_prima=data_line['valor_prima'],
                    doc_cobro=data_line['doc_cobro'],
                    fecha_ini=fecha_ini,
                    fecha_fin=data_line['fecha_fin'] or None,
                    dias=data_line['dias'],
                    telefono_1=data_line['telefono_1'],
                    telefono_2=data_line['telefono_2'],
                    telefono_3=data_line['telefono_3'],
                    ciudad=data_line['ciudad'],
                    departamento=data_line['departamento'],
                    fecha_venta=data_line['fecha_venta'],
                    fecha_nacimiento=data_line['fecha_nacimiento'],
                    tipo_trans=data_line['tipo_trans'],
                    beneficiarios=data_line['beneficiarios'],
                    genero=data_line['genero'],
                    sucursal=data_line['sucursal'],
                    tipo_cuenta=data_line['tipo_cuenta'] or None,
                    ultimos_digitos_cuenta=data_line['ultimos_digitos_cuenta'],
                    entidad_bancaria=data_line['entidad_bancaria'],
                    nombre_banco=data_line['nombre_banco'],
                    estado_debito=data_line['estado_debito'],
                    causal_rechazo=data_line['causal_rechazo'],
                    codigo_canal=data_line['codigo_canal'],
                    descripcion_canal=data_line['descripcion_canal'],
                    codigo_estrategia=data_line['codigo_estrategia'],
                    tipo_estrategia=data_line['tipo_estrategia'],
                    correo_electronico=data_line['correo_electronico'],
                    fecha_entrega_colmena=fecha_entrega_colmena,
                    mes_a_trabajar=data_line['mes_a_trabajar'],
                    id_custom=data_line['id'] or None,
                    nombre_db=data_line['nombre_db'],
                    telefono=data_line['telefono'] or None,
                    whatsapp=data_line['whatsapp'] or None,
                    texto=data_line['texto'] or None,
                    email=data_line['email'] or None,
                    fisica=data_line['fisica'] or None,
                    mejor_canal=data_line['mejor_canal'] or None,
                    contactar_al=data_line['contactar_al'] or None
                )
                
                data_import.save()
                saved_count += 1
                
            except Exception as e:
                error_msg = f"Error saving record {data_line.get('documento', 'unknown')}: {e}"
                errors.append(error_msg)
                print(error_msg)
        
        return saved_count, errors