from ..model import db

class categorie(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer,primary_key=True)
    libelle = db.Column(db.String(200), unique =True, nullable=False)
    img = db.Column(db.Text(1000), nullable=True, default="/static/uploads/")
    isArchived = db.Column(db.Integer,default=0)
    #OneToMany=> annonce
    annonces = db.relationship("annonce", backref="categorie", lazy="joined")
    #OneToMany=> souscategorie
    souscategories = db.relationship("souscategorie", backref="categorie", lazy="joined")
    #ManyToOne => User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    createBy = db.relationship("user", backref="categorie", lazy="joined")

    def  __init__(self,libelle,img="",isArchived=0):
        self.libelle = libelle
        self.img = img
        self.isArchived = isArchived

    def __repr__(self) -> str:
        return "{}".format(self.libelle)
    
def getLibelle(self):
    return self.libelle

def getId(self):
    return self.id    

def getAll():
    return categorie.query.filter_by(isArchived=0).all()

def getById(id):
    return categorie.query.filter_by(id=id,isArchived=0).first()
