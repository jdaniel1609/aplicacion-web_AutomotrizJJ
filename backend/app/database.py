import sqlite3
import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

DATABASE_PATH = "automotriz_jj.db"

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Inicializa la base de datos y crea las tablas si no existen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla: vendedores (ACTUALIZADA)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'vendedor',
                codigo_vendedor TEXT UNIQUE NOT NULL,
                sucursal_provincia TEXT NOT NULL,
                sucursal_distrito TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para vendedores
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_username ON vendedores(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_codigo ON vendedores(codigo_vendedor)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_provincia ON vendedores(sucursal_provincia)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_distrito ON vendedores(sucursal_distrito)')
        
        # Tabla: autos_disponibles (SIN CAMBIOS)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autos_disponibles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER NOT NULL,
                precio_referencial REAL,
                stock INTEGER DEFAULT 25,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para autos_disponibles
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_marca ON autos_disponibles(marca)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_modelo ON autos_disponibles(modelo)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_anio ON autos_disponibles(anio)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_active ON autos_disponibles(is_active)')
        
        # Tabla: registro_venta (ACTUALIZADA)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registro_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vendedor_id INTEGER NOT NULL,
                auto_id INTEGER NOT NULL,
                tipo_compra TEXT NOT NULL,
                monto_fisco TEXT NOT NULL,
                nombre_comprador TEXT NOT NULL,
                dni_comprador TEXT NOT NULL,
                contacto_comprador TEXT NOT NULL,
                sucursal_provincia TEXT NOT NULL,
                sucursal_distrito TEXT NOT NULL,
                nombre_vendedor TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE CASCADE,
                FOREIGN KEY (auto_id) REFERENCES autos_disponibles(id) ON DELETE CASCADE
            )
        ''')
        
        # Índices para registro_venta
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_fecha ON registro_venta(fecha_venta)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_vendedor ON registro_venta(vendedor_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_auto ON registro_venta(auto_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_tipo_compra ON registro_venta(tipo_compra)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_dni ON registro_venta(dni_comprador)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_provincia ON registro_venta(sucursal_provincia)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_distrito ON registro_venta(sucursal_distrito)')
        
        conn.commit()
        logger.info("✅ Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def seed_initial_data():
    """Inserta datos iniciales en las tablas"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si ya existen datos
        cursor.execute("SELECT COUNT(*) FROM vendedores")
        if cursor.fetchone()[0] > 0:
            logger.info("Los datos iniciales ya existen, omitiendo seed...")
            return
        
        import hashlib
        
        # ============================================
        # VENDEDORES (12 vendedores)
        # ============================================
        vendedores = [
            # LIMA - 4 distritos (2 vendedores por distrito)
            ('CARLOS', 'carlos2020', 'Carlos Mendoza', 'carlos@automotrizjj.com', 'vendedor', 'VEN001', 'LIMA', 'Miraflores'),
            ('SOFIA', 'sofia2020', 'Sofía Vargas', 'sofia@automotrizjj.com', 'vendedor', 'VEN002', 'LIMA', 'Miraflores'),
            ('MIGUEL', 'miguel2020', 'Miguel Ángel Rojas', 'miguel@automotrizjj.com', 'vendedor', 'VEN003', 'LIMA', 'San Isidro'),
            ('LAURA', 'laura2020', 'Laura Patricia Díaz', 'laura@automotrizjj.com', 'vendedor', 'VEN004', 'LIMA', 'San Isidro'),
            ('DIEGO', 'diego2020', 'Diego Alonso Cruz', 'diego@automotrizjj.com', 'vendedor', 'VEN005', 'LIMA', 'Surco'),
            ('ANDREA', 'andrea2020', 'Andrea Fernanda López', 'andrea@automotrizjj.com', 'vendedor', 'VEN006', 'LIMA', 'Surco'),
            ('ROBERTO', 'roberto2020', 'Roberto Carlos Silva', 'roberto@automotrizjj.com', 'vendedor', 'VEN007', 'LIMA', 'La Molina'),
            ('PATRICIA', 'patricia2020', 'Patricia Elena Torres', 'patricia@automotrizjj.com', 'vendedor', 'VEN008', 'LIMA', 'La Molina'),
            
            # PIURA - 2 distritos (2 vendedores por distrito)
            ('FERNANDO', 'fernando2020', 'Fernando Javier Campos', 'fernando@automotrizjj.com', 'vendedor', 'VEN009', 'PIURA', 'Piura Centro'),
            ('VALENTINA', 'valentina2020', 'Valentina Morales', 'valentina@automotrizjj.com', 'vendedor', 'VEN010', 'PIURA', 'Piura Centro'),
            
            # AYACUCHO - 2 distritos
            ('MARCO', 'marco2020', 'Marco Antonio Quispe', 'marco@automotrizjj.com', 'vendedor', 'VEN011', 'AYACUCHO', 'Ayacucho Centro'),
            ('CARMEN', 'carmen2020', 'Carmen Rosa Huamán', 'carmen@automotrizjj.com', 'vendedor', 'VEN012', 'AYACUCHO', 'Ayacucho Centro'),
        ]
        
        for username, password, full_name, email, role, codigo, provincia, distrito in vendedores:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO vendedores (username, password_hash, full_name, email, role, codigo_vendedor, sucursal_provincia, sucursal_distrito)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, full_name, email, role, codigo, provincia, distrito))
        
        # ============================================
        # AUTOS DISPONIBLES (2024 y 2025)
        # ============================================
        autos_base = [
            ('Toyota', 'Corolla', 85000.00),
            ('Toyota', 'Yaris', 65000.00),
            ('Toyota', 'RAV4', 125000.00),
            ('Honda', 'Civic', 90000.00),
            ('Honda', 'CR-V', 130000.00),
            ('Honda', 'Accord', 110000.00),
            ('Nissan', 'Sentra', 75000.00),
            ('Nissan', 'Kicks', 80000.00),
            ('Nissan', 'X-Trail', 120000.00),
            ('Hyundai', 'Elantra', 78000.00),
            ('Hyundai', 'Tucson', 115000.00),
            ('Hyundai', 'Accent', 62000.00),
            ('Mazda', '3', 88000.00),
            ('Mazda', 'CX-5', 128000.00),
            ('Mazda', '2', 68000.00),
            ('Kia', 'Forte', 76000.00),
            ('Kia', 'Sportage', 122000.00),
            ('Kia', 'Rio', 64000.00),
            ('Chevrolet', 'Cruze', 82000.00),
            ('Chevrolet', 'Tracker', 95000.00),
            ('Ford', 'Focus', 79000.00),
            ('Ford', 'Escape', 118000.00),
            ('BMW', 'Serie 3', 180000.00),
            ('BMW', 'X3', 220000.00)
        ]
        
        # Insertar autos 2024
        for marca, modelo, precio in autos_base:
            cursor.execute('''
                INSERT INTO autos_disponibles (marca, modelo, anio, precio_referencial, stock)
                VALUES (?, ?, ?, ?, ?)
            ''', (marca, modelo, 2024, precio, 25))
        
        # Insertar autos 2025 (con incremento de precio aleatorio)
        for marca, modelo, precio_2024 in autos_base:
            incremento = random.randrange(25000, 75001, 10)  # Números entre 25000-75000 terminados en 0
            precio_2025 = precio_2024 + incremento
            cursor.execute('''
                INSERT INTO autos_disponibles (marca, modelo, anio, precio_referencial, stock)
                VALUES (?, ?, ?, ?, ?)
            ''', (marca, modelo, 2025, precio_2025, 25))
        
        conn.commit()
        
        # ============================================
        # REGISTRO DE VENTAS (432 registros)
        # ============================================
        # Obtener IDs de vendedores y autos
        cursor.execute('SELECT id FROM vendedores')
        vendedor_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute('SELECT id, marca, modelo, anio, precio_referencial FROM autos_disponibles')
        autos = cursor.fetchall()
        
        tipos_compra = ['Cash', 'Crédito']
        nombres = ['Juan Pérez', 'María García', 'Carlos López', 'Ana Martínez', 'Luis Rodríguez', 
                   'Carmen Silva', 'José Torres', 'Elena Flores', 'Pedro Ramírez', 'Isabel Castro']
        
        # Generar 432 ventas
        ventas_por_auto = {}
        for auto in autos:
            auto_id = auto[0]
            num_ventas = random.randint(5, 20)
            ventas_por_auto[auto_id] = (num_ventas, auto)
        
        total_ventas = 0
        fecha_inicio = datetime.now() - timedelta(days=180)  # Últimos 6 meses
        
        for auto_id, (num_ventas, auto_info) in ventas_por_auto.items():
            for _ in range(num_ventas):
                if total_ventas >= 432:
                    break
                
                # Datos aleatorios
                vendedor_id = random.choice(vendedor_ids)
                
                # Obtener datos del vendedor
                cursor.execute('''
                    SELECT full_name, sucursal_provincia, sucursal_distrito 
                    FROM vendedores WHERE id = ?
                ''', (vendedor_id,))
                vendedor_data = cursor.fetchone()
                
                tipo_compra = random.choice(tipos_compra)
                nombre_comprador = random.choice(nombres)
                dni_comprador = str(random.randint(10000000, 99999999))
                contacto_comprador = f"9{random.randint(10000000, 99999999)}"
                
                # Calcular precio con variación del ±10%
                precio_base = auto_info[4]
                variacion = random.uniform(0.9, 1.1)
                monto = int(precio_base * variacion)
                monto_texto = f"S/. {monto:,.2f}"
                
                # Fecha aleatoria en los últimos 6 meses
                dias_atras = random.randint(0, 180)
                fecha_venta = fecha_inicio + timedelta(days=dias_atras)
                
                cursor.execute('''
                    INSERT INTO registro_venta (
                        fecha_venta, vendedor_id, auto_id, tipo_compra, monto_fisco,
                        nombre_comprador, dni_comprador, contacto_comprador,
                        sucursal_provincia, sucursal_distrito, nombre_vendedor
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    fecha_venta, vendedor_id, auto_id, tipo_compra, monto_texto,
                    nombre_comprador, dni_comprador, contacto_comprador,
                    vendedor_data[1], vendedor_data[2], vendedor_data[0]
                ))
                
                total_ventas += 1
            
            if total_ventas >= 432:
                break
        
        conn.commit()
        
        logger.info("✅ Datos iniciales insertados correctamente")
        logger.info(f"   - {len(vendedores)} vendedores")
        logger.info(f"   - {len(autos_base) * 2} autos disponibles (2024 y 2025)")
        logger.info(f"   - {total_ventas} registros de ventas")
        
    except Exception as e:
        logger.error(f"❌ Error al insertar datos iniciales: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()