from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Crea un archivo llamado sistema_b.db en esta misma carpeta
SQLALCHEMY_DATABASE_URL = "sqlite:///./sistema_b.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Tabla de ejemplo para el sistema B
class RegistroB(Base):
    __tablename__ = "datos_recibidos"
    id = Column(Integer, primary_key=True, index=True)
    dato_descifrado = Column(String, index=True)

# Crea el archivo físico
Base.metadata.create_all(bind=engine)
print("Base de datos del Sistema B inicializada con éxito.")