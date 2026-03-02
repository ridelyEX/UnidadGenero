# organizaciones/management/commands/importar_personas.py
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from organizaciones.models import Persona


class Command(BaseCommand):
    help = 'Importa personas desde un archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'archivo',
            type=str,
            help='Ruta del archivo Excel a importar'
        )

    def handle(self, *args, **options):
        archivo = options['archivo']

        if not os.path.exists(archivo):
            self.stdout.write(self.style.ERROR(f'El archivo {archivo} no existe'))
            return

        try:
            df = pd.read_excel(archivo)

            columnas_requeridas = ['nombre']

            for col in columnas_requeridas:
                if col not in df.columns:
                    self.stdout.write(self.style.ERROR(f'Falta la columna requerida: {col}'))
                    return

            personas_creadas = 0
            errores = 0

            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        datos = {
                            'nombre': str(row['nombre']).strip(),
                        }

                        if 'num_empleado' in row and pd.notna(row['num_empleado']):
                            datos['num_empleado'] = str(row['num_empleado']).strip()

                        if 'departamento' in row and pd.notna(row['departamento']):
                            datos['departamento'] = str(row['departamento']).strip()

                        if 'puesto' in row and pd.notna(row['puesto']):
                            datos['puesto'] = str(row['puesto']).strip()

                        # Crear persona (sin update_or_create porque no hay campo único)
                        persona = Persona.objects.create(**datos)
                        personas_creadas += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'✓ Creada: {persona.nombre}'
                        ))

                    except Exception as e:
                        errores += 1
                        self.stdout.write(self.style.ERROR(
                            f'✗ Error en fila {index + 2}: {str(e)}'
                        ))

            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS(f'Personas creadas: {personas_creadas}'))
            if errores > 0:
                self.stdout.write(self.style.ERROR(f'Errores: {errores}'))
            self.stdout.write(self.style.SUCCESS('='*50))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al procesar el archivo: {str(e)}'))