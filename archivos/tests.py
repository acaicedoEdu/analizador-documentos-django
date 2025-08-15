import os
import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from datetime import datetime
from .models import DataImport
from .processors import FileProcessor

class IntegrationTest(TestCase):
    
    def setUp(self):
        self.realistic_line = (
            "0123456789"    
            "CC "          
            "123456789012345"  
            "JUAN PEREZ GOMEZ                                                                                   "  
            "SEG01POL123456"   
            "A1000000.00      "  
            "50000.00           "           
            "DOC12345678  "    
            "2025-05-29         "  
            "30   "            
            "3001234567     "  
            "BOGOTA                                              " 
            "CUNDINAMARCA                                        " 
            "2025-05-291990-01-01VENNONE                                                                                                 " 
            "MPRINCIPAL                                         " 
            "1234              " 
            "BANCO1 "          
            "BANCO NACIONAL                                " 
            "ACTIVO    "       
            + "A" * 990        
        )
        
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        self.test_file_path = os.path.join(upload_dir, 'PRUEBA_20250529.txt')
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(self.realistic_line + '\n')
    
    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
    
    def test_complete_processing_flow(self):
        processor = FileProcessor()
        
        # 1. Procesar archivo
        records = processor.process_file(self.test_file_path)
        self.assertTrue(len(records) > 0)
        
        record = records[0]
        
        # 2. Verificar extracción de datos
        self.assertEqual(record['tipo_documento'], 'CC')
        self.assertIn('JUAN PEREZ', record['nombre'])
        self.assertEqual(record['producto'], 'SEG01')
        
        # 3. Guardar en base de datos
        saved_count, errors = processor.save_to_database(records)
        self.assertEqual(saved_count, 1)
        self.assertEqual(len(errors), 0)
        
        # 4. Verificar que se guardó correctamente
        saved_record = DataImport.objects.get(documento='123456789012345')
        self.assertEqual(saved_record.tipo_documento, 'CC')
        self.assertIn('JUAN PEREZ', saved_record.nombre)
        
        # 5. Generar CSV
        csv_path = os.path.join(settings.MEDIA_ROOT, 'test_output.csv')
        csv_saved = processor.save_to_csv(records, csv_path)
        self.assertTrue(csv_saved)
        self.assertTrue(os.path.exists(csv_path))
        
        # Limpiar archivo CSV de prueba
        if os.path.exists(csv_path):
            os.remove(csv_path)