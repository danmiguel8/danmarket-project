from ..model import db

class souscategorie(db.Model):
    __tablename__ = "souscategories"
    id = db.Column(db.Integer,primary_key=True)
    libelle = db.Column(db.String(200), unique =True, nullable=False)
    isArchived = db.Column(db.Integer,default=0)
    #ManyToOne => Categorie
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    categories = db.relationship("categorie", backref="souscategorie", lazy="joined")
    #OneToMany=> Annonce
    annonces = db.relationship("annonce", backref="souscategorie", lazy="joined")
    #ManyToOne => User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    createBy = db.relationship("user", backref="souscategorie", lazy="joined")

    def  __init__(self,libelle):
        self.libelle = libelle

    def __repr__(self) -> str:
        return "{}".format(self.libelle)
    
def getLibelle(self):
    return self.libelle

def getId(self):
    return self.id    

def getAll():
    return souscategorie.query.filter_by(isArchived=0).all()

def getById(id):
    return souscategorie.query.filter_by(id=id,isArchived=0).first()