from tabnanny import filename_only
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from .processors import FileProcessor
from django.conf import settings

# Create your views here.
class AnalyzeArchiveView(APIView):
    def post(self, request):
        try:
            archivename = request.data.get('archivename')

            if not archivename:
                return Response({
                'error': 'El parámetro archivename es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
            # Se construlle la ruta completa del archivo
            archive_path = settings.UPLOADS_DIR / archivename
            print(archive_path)
            if not archive_path.exists():
                return Response({
                    'error': f'El archivo {archivename} no existe'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Procesar el archivo
            processor = FileProcessor()
            data_json = processor.process_archive(archive_path)
            
            if not data_json:
                return Response({
                    'error': 'No se pudieron extraer datos del archivo'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generar CSV
            csv_archivename = f"processed_{archivename.replace('.txt', '.csv')}"
            csv_path = settings.BASE_DIR / 'output' / csv_archivename
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            
            csv_saved = processor.save_csv(data_json, csv_path)
            
            # Guardar en base de datos
            saved_count, errors = processor.save_db(data_json)
            
            return Response({
                'success': True,
                'message': f'Archivo procesado exitosamente',
                'data': {
                    'archivename': archivename,
                    'link_csv_generated': f"http://127.0.0.1:8000/output/{csv_archivename}" if csv_saved else csv_saved,
                    'count_data_bd_saved': saved_count,
                    'errors': errors
                }
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': f'Error interno del servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)