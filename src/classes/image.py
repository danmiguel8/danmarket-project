from ..model import db

class image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer,primary_key=True)
    img = db.Column(db.Text(1000), nullable=False, default="/static/uploads/")  
    isArchived = db.Column(db.Integer,default=0)
    #ManyToOne => annonce
    annonce_id = db.Column(db.Integer, db.ForeignKey("annonces.id"))
    annonces = db.relationship("annonce", backref="image", lazy="joined")

    def __init__(self,img,annonce_id, isArchived=0):
        self.img = img
        self.annonce_id = annonce_id
        self.isArchived = isArchived

    def __repr__(self) -> str:
        return "{}".format(self.img)
    
def getAll():
    return image.query.filter_by(isArchived=0).all()

def getById(id):
    return image.query.filter_by(id=id,isArchived=0).first()

def getImagesByAnnonceId(idAnnonce):
    return image.query.filter_by(annonce_id=idAnnonce,isArchived=0).all()