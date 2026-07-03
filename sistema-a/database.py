from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Crea un archivo llamado sistema_a.db en esta misma carpeta
SQLALCHEMY_DATABASE_URL = "sqlite:///./sistema_a.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Creamos una tabla de ejemplo para demostrar que funciona
class RegistroA(Base):
    __tablename__ = "registros"
    id = Column(Integer, primary_key=True, index=True)
    mensaje = Column(String, index=True)

# Esta línea es la que crea el archivo físico de la base de datos
Base.metadata.create_all(bind=engine)
print("Base de datos del Sistema A inicializada con éxito.")