from ..model import db

class motcles(db.Model):
    __tablename__ = "motcles"
    id = db.Column(db.Integer,primary_key=True)
    libelle = db.Column(db.String(200), unique =True, nullable=False)
    isArchived = db.Column(db.Integer,default=0)

    def  __init__(self,libelle):
        self.libelle = libelle
    
def getLibelle(self):
    return self.libelle

def getId(self):
    return self.id    

def getAll():
    return motcles.query.filter_by(isArchived=0).all()

def getById(id):
    return motcles.query.filter_by(id=id,isArchived=0).first()