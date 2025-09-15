from sqlalchemy import (
    Column, CheckConstraint, Integer, SmallInteger, String, Numeric, CHAR, Boolean, ForeignKey,
    DateTime, Enum, Index, UniqueConstraint, Text
)
from sqlalchemy.sql import func, text
from sqlalchemy.orm import validates, relationship
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
    rasgos_tea = Column(String(2)) 
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
    #AÑADIR CONSTRAINTS, VALIDADORES INDEX

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
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
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

    # ORM: relación 1:N con usuario
    usuarios = relationship(
        "Usuario",
        back_populates="empresa",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # ---- Constraints a nivel BD (regex de teléfono y correo)
    __table_args__ = (
        CheckConstraint(
            "numero_contacto ~ '^\\+?[0-9]{7,15}$'",
            name="chk_empresa_telefono_formato",
        ),
        CheckConstraint(
            "correo ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$'",
            name="chk_empresa_correo_formato",
        ),
        Index("ix_empresa_is_active", "is_active"),
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
    @staticmethod
    def _is_valid_phone(phone: str) -> bool:
        return bool(re.match(r'^\+?[0-9]{7,15}$', phone))

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return bool(re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$', email, re.IGNORECASE))

    
RolUsuarioEnum = Enum("ADMIN", "OPERADOR", name="rol_usuario")  # Enum en PostgreSQL

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)

    empresa_id = Column(
        Integer,
        ForeignKey("empresa.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    email = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=False)

    nombre = Column(Text, nullable=False)
    rol = Column(RolUsuarioEnum, nullable=False)

    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    last_login = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("date_trunc('second', now())"),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("date_trunc('second', now())"),
        server_onupdate=text("date_trunc('second', now())"),
        onupdate=func.now(),  # pylint: disable=E1102
        nullable=False,
    )

    # ORM: relación inversa
    empresa = relationship("Empresa", back_populates="usuarios", lazy="joined")

    __table_args__ = (
        # Unicidad por tenant
        UniqueConstraint("empresa_id", "email", name="uq_usuario_email_por_empresa"),
        UniqueConstraint("empresa_id", "username", name="uq_usuario_username_por_empresa"),

        # Checks de formato 
        CheckConstraint(
            "email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$'",
            name="chk_usuario_email_formato",
        ),
        # Índices útiles
        Index("ix_usuario_is_active", "is_active"),
        Index("ix_usuario_rol", "rol"),
    )

    # -------- API de contraseñas
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
    

    # -------- Validadores Python
    @validates("email")
    def validate_email(self, key, email):
        if not email or not Empresa._is_valid_email(email):
            raise ValueError("El email del usuario no es válido.")
        return email

    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError("El username no puede estar vacío.")
        return username
    