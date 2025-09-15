from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import Empresa, Usuario  
from app.db.database import SessionLocal

# Datos de la empresa por defecto
empresa_default = {
    "nombre": "Plena-MENTE",
    "numero_contacto": "+51937562487",
    "correo": "plenamentetrujillo@gmail.com",
    "ciudad": "Trujillo",
    "pais": "Perú",
    "direccion": "Huayna Capac 713, urb. Santa María",
}

# Datos del usuario admin por defecto
admin_default = {
    "email": "ernestosaniel123@gmail.com",
    "username": "ECastro",
    "nombre": "Ernesto Castro",
    "rol": "ADMIN",
    # se recomienda rotarla por ENV/secret en producción
    "password_plano": "Admin123",
}


def crear_empresa_default(db: Session) -> Empresa:
    """
    Crea la empresa por defecto si no existe y la retorna.
    Si ya existe, retorna la primera (según tu modelo de negocio, podrías filtrar por nombre).
    """
    empresa = db.query(Empresa).first()
    if empresa:
        print("La empresa ya está registrada.")
        return empresa

    empresa = Empresa(
        nombre=empresa_default["nombre"],
        numero_contacto=empresa_default["numero_contacto"],
        correo=empresa_default["correo"],
        ciudad=empresa_default["ciudad"],
        pais=empresa_default["pais"],
        direccion=empresa_default["direccion"],
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    print("Empresa por defecto creada.")
    return empresa


def crear_admin_default(db: Session, empresa: Empresa) -> Usuario:
    """
    Crea un usuario ADMIN por defecto para la empresa dada si no existe ya
    (según combinación empresa_id + username/email).
    """
    # ¿Ya hay un admin con ese username o email en este tenant?
    existente = (
        db.query(Usuario)
        .filter(
            Usuario.empresa_id == empresa.id,
            (Usuario.username == admin_default["username"]) | (Usuario.email == admin_default["email"]),
        )
        .first()
    )
    if existente:
        print("Usuario ADMIN por defecto ya existe.")
        return existente

    admin = Usuario(
        empresa_id=empresa.id,
        email=admin_default["email"],
        username=admin_default["username"],
        nombre=admin_default["nombre"],
        rol=admin_default["rol"],
    )
    admin.set_password(admin_default["password_plano"])
    db.add(admin)

    try:
        db.commit()
        db.refresh(admin)
        print("Usuario ADMIN por defecto creado.")
        return admin
    except IntegrityError as ie:
        db.rollback()
        # En caso de colisión por unicidad entre llamadas concurrentes
        print(f"Colisión de unicidad al crear el admin por defecto: {ie}")
        # Reintenta leerlo
        admin = (
            db.query(Usuario)
            .filter(
                Usuario.empresa_id == empresa.id,
                (Usuario.username == admin_default["username"]) | (Usuario.email == admin_default["email"]),
            )
            .first()
        )
        return admin


def init_empresa():
    db = SessionLocal()
    try:
        empresa = crear_empresa_default(db)
        crear_admin_default(db, empresa)
    except Exception as e:
        db.rollback()
        print(f"Error al inicializar empresa/usuario admin: {e}")
        raise
    finally:
        db.close()
