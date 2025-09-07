from sqlalchemy import (
    Column, Integer, SmallInteger, String, Numeric, CHAR, Boolean, ForeignKey,
    DateTime, Text
)
from sqlalchemy.sql import func, text
from sqlalchemy.orm import validates
from passlib.context import CryptContext
from datetime import datetime, timezone
import re
from .database import Base

class Evaluacion(Base):
    __tablename__ = "evaluacion"

    id = Column(Integer, primary_key=True, index=True)
    # Falta agregar id de la empresa
    edad = Column(SmallInteger)
    sexo = Column(CHAR(1))

    a1 = Column(SmallInteger); a2 = Column(SmallInteger); a3 = Column(SmallInteger)
    a4 = Column(SmallInteger); a5 = Column(SmallInteger); a6 = Column(SmallInteger)
    a7 = Column(SmallInteger); a8 = Column(SmallInteger); a9 = Column(SmallInteger)
    a10 = Column(SmallInteger)

    qchat_resultado = Column(SmallInteger)

    trastorno_habla = Column(String(2))
    trastorno_aprendizaje = Column(String(2))
    trastorno_genetico = Column(String(2))
    trastorno_depresion = Column(String(2))
    retraso_global_intelectual = Column(String(2))
    problemas_comportamiento = Column(String(2))
    trastorno_ansiedad = Column(String(2))
    familiar_autista = Column(String(2))

    porc_comorbilidad = Column(Numeric(3, 2))
    porc_deficiencia_social_interactiva = Column(Numeric(3, 2))
    porc_deficiencia_comunicativa = Column(Numeric(3, 2))

    perfil_clinico = Column(String(30))
    rasgos_tea = Column(String(2))  #'Si' o 'No' 
    nivel_confianza = Column(Numeric(3, 2))

    hora_inicio = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc).replace(microsecond=0),
        nullable=False
    )
    hora_fin = Column(DateTime(timezone=True), nullable=False)
    duracion_minutos = Column(SmallInteger, nullable=False)

    # Validación
    validado_por_empresa = Column(Boolean, nullable=False, server_default=text("false"))
    validado_at = Column(DateTime(timezone=True))
    
    # Contacto
    contacto_email = Column(String(255), nullable=True) # No debería ser NULL
    contacto_telefono = Column(String(20), nullable=True)        # TEXT en BD; String aquí ok
    preferencia_contacto = Column(String, server_default=text("'email'"))

    # metadata
    is_active  = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("date_trunc('second', now())"),
        nullable=False,
    )

 # Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)  # Longitud específica
    numero_contacto = Column(String(20), nullable=False)  # Longitud para el teléfono
    correo = Column(String(255), unique=True, nullable=False)  # Longitud para el correo
    ciudad = Column(String(100), nullable=False)
    pais = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)  # Longitud para el username
    password_hash = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("date_trunc('second', now())"),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("date_trunc('second', now())"),
        server_onupdate=text("date_trunc('second', now())"),
        # opcional, refuerza cuando el UPDATE viene del ORM:
        onupdate=func.now(),# pylint: disable=E1102
        nullable=False,
    )

    # Validaciones para el formato de los campos
    @validates("numero_contacto")
    def validate_telefono(self, key, numero_contacto):
        if numero_contacto and not self._is_valid_phone(numero_contacto):
            raise ValueError("El formato del número de teléfono es incorrecto.")
        return numero_contacto

    @validates("correo")
    def validate_correo(self, key, correo):
        if correo and not self._is_valid_email(correo):
            raise ValueError("El formato del correo electrónico es incorrecto.")
        return correo

    # Métodos para validar formato (puedes usar expresiones regulares o la librería)
    def _is_valid_phone(self, phone):
        return bool(re.match(r'^\+?[0-9]{7,15}$', phone))

    def _is_valid_email(self, email):
        return bool(re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', email, re.IGNORECASE))

    # Método para hashear la contraseña antes de guardarla
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    # Método para verificar la contraseña
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)