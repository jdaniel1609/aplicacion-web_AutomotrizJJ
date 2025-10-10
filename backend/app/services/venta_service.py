import logging
from typing import List, Optional, Dict
from app.database import get_db_connection
from datetime import datetime

logger = logging.getLogger(__name__)


def get_autos_disponibles(search: Optional[str] = None) -> List[Dict]:
    """
    Obtiene lista de autos disponibles, con búsqueda opcional
    
    Args:
        search: Término de búsqueda (opcional)
        
    Returns:
        Lista de autos disponibles
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if search:
            # Búsqueda por marca, modelo o año
            cursor.execute('''
                SELECT id, marca, modelo, anio, precio_referencial, stock
                FROM autos_disponibles
                WHERE is_active = 1 AND stock > 0
                AND (
                    marca LIKE ? OR 
                    modelo LIKE ? OR 
                    CAST(anio AS TEXT) LIKE ?
                )
                ORDER BY marca, modelo, anio
            ''', (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            cursor.execute('''
                SELECT id, marca, modelo, anio, precio_referencial, stock
                FROM autos_disponibles
                WHERE is_active = 1 AND stock > 0
                ORDER BY marca, modelo, anio
            ''')
        
        autos = [dict(row) for row in cursor.fetchall()]
        return autos
        
    except Exception as e:
        logger.error(f"❌ Error al obtener autos disponibles: {e}")
        return []
    finally:
        conn.close()


def get_tipos_compra() -> List[Dict]:
    """
    Obtiene lista de tipos de compra disponibles
    
    Returns:
        Lista de tipos de compra
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id, tipo, descripcion FROM tipo_compra ORDER BY tipo')
        tipos = [dict(row) for row in cursor.fetchall()]
        return tipos
        
    except Exception as e:
        logger.error(f"❌ Error al obtener tipos de compra: {e}")
        return []
    finally:
        conn.close()


def registrar_venta(
    vendedor_id: int,
    auto_id: int,
    tipo_compra_id: int,
    monto_fisco: str,
    nombre_comprador: str,
    dni_comprador: str,
    contacto_comprador: str,
    sucursal: str,
    nombre_vendedor: str
) -> Optional[int]:
    """
    Registra una nueva venta en la base de datos
    
    Returns:
        ID de la venta registrada o None si hay error
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO registro_venta (
                vendedor_id, auto_id, tipo_compra_id, monto_fisco,
                nombre_comprador, dni_comprador, contacto_comprador,
                sucursal, nombre_vendedor, fecha_venta
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vendedor_id, auto_id, tipo_compra_id, monto_fisco,
            nombre_comprador, dni_comprador, contacto_comprador,
            sucursal, nombre_vendedor, datetime.now()
        ))
        
        venta_id = cursor.lastrowid
        conn.commit()
        
        logger.info(f"✅ Venta registrada exitosamente - ID: {venta_id}")
        logger.info(f"   - Vendedor: {nombre_vendedor} ({sucursal})")
        logger.info(f"   - Comprador: {nombre_comprador} (DNI: {dni_comprador})")
        logger.info(f"   - Monto: {monto_fisco}")
        
        return venta_id
        
    except Exception as e:
        logger.error(f"❌ Error al registrar venta: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def get_ventas_by_vendedor(vendedor_id: int, limit: int = 50) -> List[Dict]:
    """
    Obtiene las últimas ventas de un vendedor
    
    Args:
        vendedor_id: ID del vendedor
        limit: Número máximo de ventas a retornar
        
    Returns:
        Lista de ventas
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT 
                rv.id,
                rv.fecha_venta,
                rv.monto_fisco,
                rv.nombre_comprador,
                rv.dni_comprador,
                rv.contacto_comprador,
                a.marca || ' ' || a.modelo || ' ' || a.anio AS auto,
                tc.tipo AS tipo_compra,
                rv.sucursal
            FROM registro_venta rv
            JOIN autos_disponibles a ON rv.auto_id = a.id
            JOIN tipo_compra tc ON rv.tipo_compra_id = tc.id
            WHERE rv.vendedor_id = ?
            ORDER BY rv.fecha_venta DESC
            LIMIT ?
        ''', (vendedor_id, limit))
        
        ventas = [dict(row) for row in cursor.fetchall()]
        return ventas
        
    except Exception as e:
        logger.error(f"❌ Error al obtener ventas del vendedor: {e}")
        return []
    finally:
        conn.close()