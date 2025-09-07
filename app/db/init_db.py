from sqlalchemy.orm import Session
from app.db.models import Empresa
from app.db.database import SessionLocal

# Datos de la empresa por defecto
empresa_default = {
    "nombre": "Plena-MENTE",
    "numero_contacto": "+51937562487",
    "correo": "plenamentetrujillo@gmail.com",
    "ciudad": "Trujillo",
    "pais": "Perú",
    "direccion": "Huayna Capac 713, urb. Santa María",
    "username": "plenamente",
    "password": "admin123",  # Esto debería ser un password seguro
}

def crear_empresa_default(db: Session):
    # Verificar si la empresa ya existe
    empresa_existente = db.query(Empresa).first()
    if not empresa_existente:
        # Crear la empresa por defecto si no existe
        empresa = Empresa(
            nombre=empresa_default["nombre"],
            numero_contacto=empresa_default["numero_contacto"],
            correo=empresa_default["correo"],
            ciudad=empresa_default["ciudad"],
            pais=empresa_default["pais"],
            direccion=empresa_default["direccion"],
            username=empresa_default["username"],
        )
        # Hashear la contraseña antes de guardar
        empresa.set_password(empresa_default["password"])

        db.add(empresa)
        db.commit()
        db.refresh(empresa)
        print("Empresa por defecto creada.")
    else:
        print("La empresa ya está registrada.")


def init_empresa():
    db = SessionLocal()
    try:
        # Crear la empresa por defecto
        crear_empresa_default(db)
    except Exception as e:
        db.rollback()
        print(f"Error al crear la empresa: {e}")
    finally:
        db.close()
