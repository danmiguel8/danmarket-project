from ..model import db
from ..classes import annonce 

class favoris(db.Model):
    __tablename__ = 'favoris'
    id = db.Column(db.Integer, primary_key=True)
    #ManyToOne => User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #ManyToOne => Annonce
    annonce_id = db.Column(db.Integer, db.ForeignKey("annonces.id"))
    isArchived = db.Column(db.Integer,default=0)

    def __init__(self,user_id:int,annonce_id:int,isArchived=0):
        self.user_id = user_id
        self.annonce_id = annonce_id
        self.isArchived = isArchived

def getAll():
    return favoris.query.filter_by(isArchived=0).all()

def getById(id):
    return favoris.query.filter_by(id=id,isArchived=0).first()

def getAnnonceFavoriteById(annonceId):
    return favoris.query.filter_by(annonce_id=annonceId,isArchived=0).all()

def getFavorisByUser(userId):
    favs = favoris.query.filter_by(user_id=userId,isArchived=0).all()
    result = []
    for f in favs :  
        an = annonce.getById(f.annonce_id)
        if an != None :  
            result.append(an)
    return result

def updateOrInsertByUserAndAnnonce(userId,annonceId): 
    fav = favoris.query.filter_by(user_id=userId,annonce_id=annonceId).first()
    if fav is None:
        fav = favoris(userId,annonceId)
        db.session.add(fav)
    else:
        if fav.isArchived == 0 :
            fav.isArchived = 1
        else:
            fav.isArchived = 0
    db.session.commit()


