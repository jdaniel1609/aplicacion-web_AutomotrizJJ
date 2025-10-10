import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DATABASE_PATH = "automotriz_jj.db"

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
    return conn

def init_database():
    """Inicializa la base de datos y crea las tablas si no existen"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Tabla: vendedores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'vendedor',
                codigo_vendedor TEXT UNIQUE NOT NULL,
                sucursal TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para vendedores
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_username ON vendedores(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_codigo ON vendedores(codigo_vendedor)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_vendedores_sucursal ON vendedores(sucursal)')
        
        # Tabla: tipo_compra
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipo_compra (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índice para tipo_compra
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tipo_compra_tipo ON tipo_compra(tipo)')
        
        # Tabla: autos_disponibles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS autos_disponibles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio INTEGER NOT NULL,
                precio_referencial REAL,
                stock INTEGER DEFAULT 1,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para autos_disponibles
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_marca ON autos_disponibles(marca)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_modelo ON autos_disponibles(modelo)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_anio ON autos_disponibles(anio)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autos_active ON autos_disponibles(is_active)')
        
        # Tabla: registro_venta
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registro_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vendedor_id INTEGER NOT NULL,
                auto_id INTEGER NOT NULL,
                tipo_compra_id INTEGER NOT NULL,
                monto_fisco TEXT NOT NULL,
                nombre_comprador TEXT NOT NULL,
                dni_comprador TEXT NOT NULL,
                contacto_comprador TEXT NOT NULL,
                sucursal TEXT NOT NULL,
                nombre_vendedor TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE CASCADE,
                FOREIGN KEY (auto_id) REFERENCES autos_disponibles(id) ON DELETE CASCADE,
                FOREIGN KEY (tipo_compra_id) REFERENCES tipo_compra(id) ON DELETE CASCADE
            )
        ''')
        
        # Índices para registro_venta
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_fecha ON registro_venta(fecha_venta)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_vendedor ON registro_venta(vendedor_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_auto ON registro_venta(auto_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_tipo_compra ON registro_venta(tipo_compra_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_dni ON registro_venta(dni_comprador)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_venta_sucursal ON registro_venta(sucursal)')
        
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
        
        # Insertar vendedores
        vendedores = [
            ('admin', 'admin123', 'Administrador', 'admin@automotrizjj.com', 'admin', 'ADM001', 'LIMA'),
            ('OMAR', 'omar2024', 'Omar Gonzales', 'omar@automotrizjj.com', 'vendedor', 'VEN001', 'PIURA'),
            ('CIRO', 'ciro2024', 'Ciro Ramírez', 'ciro@automotrizjj.com', 'vendedor', 'VEN002', 'LIMA'),
            ('JUAN', 'juan2024', 'Juan Pérez', 'juan@automotrizjj.com', 'vendedor', 'VEN003', 'AREQUIPA'),
            ('LUCIA', 'lucia2024', 'Lucía Torres', 'lucia@automotrizjj.com', 'vendedor', 'VEN004', 'LIMA'),
            ('VALERIA', 'valeria2024', 'Valeria Sánchez', 'valeria@automotrizjj.com', 'vendedor', 'VEN005', 'PIURA'),
            ('ANGELICA', 'angelica2024', 'Angélica Flores', 'angelica@automotrizjj.com', 'vendedor', 'VEN006', 'AREQUIPA')
        ]
        
        for username, password, full_name, email, role, codigo, sucursal in vendedores:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO vendedores (username, password_hash, full_name, email, role, codigo_vendedor, sucursal)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, full_name, email, role, codigo, sucursal))
        
        # Insertar tipos de compra
        tipos_compra = [
            ('Cash', 'Pago en efectivo completo'),
            ('Crédito', 'Pago mediante financiamiento')
        ]
        
        for tipo, descripcion in tipos_compra:
            cursor.execute('INSERT INTO tipo_compra (tipo, descripcion) VALUES (?, ?)', (tipo, descripcion))
        
        # Insertar autos disponibles
        autos = [
            ('Toyota', 'Corolla', 2024, 85000.00),
            ('Toyota', 'Yaris', 2024, 65000.00),
            ('Toyota', 'RAV4', 2024, 125000.00),
            ('Honda', 'Civic', 2024, 90000.00),
            ('Honda', 'CR-V', 2024, 130000.00),
            ('Honda', 'Accord', 2024, 110000.00),
            ('Nissan', 'Sentra', 2024, 75000.00),
            ('Nissan', 'Kicks', 2024, 80000.00),
            ('Nissan', 'X-Trail', 2024, 120000.00),
            ('Hyundai', 'Elantra', 2024, 78000.00),
            ('Hyundai', 'Tucson', 2024, 115000.00),
            ('Hyundai', 'Accent', 2024, 62000.00),
            ('Mazda', '3', 2024, 88000.00),
            ('Mazda', 'CX-5', 2024, 128000.00),
            ('Mazda', '2', 2024, 68000.00),
            ('Kia', 'Forte', 2024, 76000.00),
            ('Kia', 'Sportage', 2024, 122000.00),
            ('Kia', 'Rio', 2024, 64000.00),
            ('Chevrolet', 'Cruze', 2024, 82000.00),
            ('Chevrolet', 'Tracker', 2024, 95000.00),
            ('Ford', 'Focus', 2024, 79000.00),
            ('Ford', 'Escape', 2024, 118000.00),
            ('BMW', 'Serie 3', 2024, 180000.00),
            ('BMW', 'X3', 2024, 220000.00)
        ]
        
        for marca, modelo, anio, precio in autos:
            cursor.execute('''
                INSERT INTO autos_disponibles (marca, modelo, anio, precio_referencial)
                VALUES (?, ?, ?, ?)
            ''', (marca, modelo, anio, precio))
        
        conn.commit()
        logger.info("✅ Datos iniciales insertados correctamente")
        logger.info(f"   - {len(vendedores)} vendedores")
        logger.info(f"   - {len(tipos_compra)} tipos de compra")
        logger.info(f"   - {len(autos)} autos disponibles")
        
    except Exception as e:
        logger.error(f"❌ Error al insertar datos iniciales: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()