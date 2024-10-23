from src.fonctions.functions import getDateActuelle
from ..model import db

class vendu(db.Model):
    __tablename__ = 'vendus'
    id = db.Column(db.Integer, primary_key=True)
    #ManyToOne => User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #ManyToOne => Annonce
    annonce_id = db.Column(db.Integer, db.ForeignKey("annonces.id"))
    date = db.Column(db.String(30), nullable=True, default=getDateActuelle())
    isArchived = db.Column(db.Integer,default=0)

    def __init__(self,user_id:int,annonce_id:int,isArchived=0):
        self.user_id = user_id
        self.annonce_id = annonce_id
        self.isArchived = isArchived

def getAll():
    return vendu.query.filter_by(isArchived=0).all()

def getById(id):
    return vendu.query.filter_by(id=id,isArchived=0).first()

def getAnnonceByUserId(idUser):
    return vendu.query.filter_by(user_id=idUser).order_by(vendu.id.desc()).all()

