from ..model import db  

class localite(db.Model):
    __tablename__ = 'localites'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(200), unique =True, nullable=False)
    #OneToMany=> annonce
    annonces = db.relationship("annonce", backref="localite", lazy="joined")
    isArchived = db.Column(db.Integer,default=0)

    def __init__(self,libelle,isArchived=0):
        self.libelle = libelle
        self.isArchived = isArchived
    
    def __repr__(self) -> str:
        return "{}".format(self.libelle)

def getAll():
    return localite.query.filter_by(isArchived=0).all()

def getById(id):
    return localite.query.filter_by(id=id,isArchived=0).first()