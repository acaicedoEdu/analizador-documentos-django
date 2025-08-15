from django.db import models

class DataImport(models.Model):
    tipo_documento = models.CharField(max_length=3)
    documento = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    producto = models.CharField(max_length=5)
    poliza = models.CharField(max_length=10)
    periodo = models.CharField(max_length=1)
    valor_asegurado = models.CharField(max_length=21)
    valor_prima = models.CharField(max_length=22)
    doc_cobro = models.CharField(max_length=14)
    fecha_ini = models.DateField()
    fecha_fin = models.CharField(max_length=10, blank=True, null=True)
    dias = models.CharField(max_length=5)
    telefono_1 = models.CharField(max_length=15)
    telefono_2 = models.CharField(max_length=15)
    telefono_3 = models.CharField(max_length=15)
    ciudad = models.CharField(max_length=22)
    departamento = models.CharField(max_length=22)
    fecha_venta = models.CharField(max_length=10)
    fecha_nacimiento = models.CharField(max_length=10)
    tipo_trans = models.CharField(max_length=3)
    beneficiarios = models.CharField(max_length=100)
    genero = models.CharField(max_length=1)
    sucursal = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=10, blank=True, null=True)
    ultimos_digitos_cuenta = models.CharField(max_length=7)
    entidad_bancaria = models.CharField(max_length=40)
    nombre_banco = models.CharField(max_length=40)
    estado_debito = models.CharField(max_length=15)
    causal_rechazo = models.CharField(max_length=200)
    codigo_canal = models.CharField(max_length=3)
    descripcion_canal = models.CharField(max_length=15)
    codigo_estrategia = models.CharField(max_length=15)
    tipo_estrategia = models.CharField(max_length=50)
    correo_electronico = models.CharField(max_length=50)
    fecha_entrega_colmena = models.DateField()
    mes_a_trabajar = models.CharField(max_length=2)
    id_custom = models.CharField(max_length=10, blank=True, null=True)
    nombre_db = models.CharField(max_length=100)
    telefono = models.CharField(max_length=1, blank=True, null=True)
    whatsapp = models.CharField(max_length=1, blank=True, null=True)
    texto = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=1, blank=True, null=True)
    fisica = models.CharField(max_length=1, blank=True, null=True)
    mejor_canal = models.CharField(max_length=20, blank=True, null=True)
    contactar_al = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_import'

    def __str__(self):
        return f"{self.documento} - {self.nombre}"

COLUMNS_DB = [
    'tipo_documento','documento','nombre','producto','poliza','periodo','valor_asegurado',
    'valor_prima','doc_cobro','fecha_ini','fecha_fin','dias','telefono_1','telefono_2','telefono_3',
    'ciudad','departamento','fecha_venta','fecha_nacimiento','tipo_trans','beneficiarios','genero',
    'sucursal','tipo_cuenta','ultimos_digitos_cuenta','entidad_bancaria','nombre_banco','estado_debito',
    'causal_rechazo','codigo_canal','descripcion_canal','codigo_estrategia','tipo_estrategia',
    'correo_electronico','fecha_entrega_colmena','mes_a_trabajar','id','nombre_db','telefono','whatsapp',
    'texto','email','fisica','mejor_canal','contactar_al'
]