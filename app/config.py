# app/config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Ojalasalga200.@localhost:3307/WaterFresh_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Deshabilita el seguimiento de modificaciones de objetos

    # Puedes agregar más configuraciones si las necesitas
