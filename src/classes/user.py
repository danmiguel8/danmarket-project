from ..model import db  
from passlib.hash import sha256_crypt
from ..const import constantes as c
import json

class user(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    nomComplet = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum("admin","client"))
    premium = db.Column(db.Integer,default=0)
    typePremium = db.Column(db.String(200), nullable=True)
    isArchived = db.Column(db.Integer,default=0)
    #OneToMany=> annonce
    annonces = db.relationship("annonce", backref="user", lazy="joined")
    #OneToMany=> souscategorie
    souscategories = db.relationship("souscategorie", backref="user", lazy="joined")
    #OneToMany=> categorie
    categories = db.relationship("categorie", backref="user", lazy="joined")
    #OneToMany=> favoris
    favoris = db.relationship("favoris", backref="user", lazy="joined")

    def  __init__(self,login,password,nomComplet,role,premium=0,typePremium="NONE",isArchived=0):  
        self.login = login
        self.password = password
        self.nomComplet = nomComplet
        self.role = role    
        self.premium = premium
        self.typePremium = typePremium
        self.isArchived = isArchived

    def toJson(self):
        return {
            "id" : self.id,
            "login" : self.login,
            "nomCompet" : self.nomComplet,
            "role" : self.role, 
            "prenium" : self.premium,
            "typePremium" : self.typePremium
        }
    
    def __repr__(self) -> str:
        return "{} | {}".format(self.nomComplet,self.login)
    
    
def getAll():
    return user.query.filter_by(isArchived=0).all()

def getById(id):
    return user.query.filter_by(id=id,isArchived=0).first()
    

def getUserByLoginAndPassword(log:str,passw:str):
    u = user.query.filter_by(login=log,isArchived=0).first()
    if u is None :
        return None  
    if(sha256_crypt.verify(passw,u.password)) :
        return u
    return  None

def getUserByLogin(log:str):
    return user.query.filter_by(login=log).first()

def addAbonnementToUser(id:int,aboType:str):
    u = getById(id)
    if u is None :
        return None  
    u.typePremium = aboType
    u.premium = 1
    db.session.commit()

    
    

  
