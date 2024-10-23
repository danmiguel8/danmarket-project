from ..model import db  

class annonce(db.Model):
    __tablename__ = 'annonces'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(1000), nullable=True)
    titre = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    prixpromo = db.Column(db.Float, nullable=True, default=0)
    #ManyToOne => Localite
    localites = db.relationship("localite", backref="annonce", lazy="joined")
    localite_id = db.Column(db.Integer, db.ForeignKey("localites.id"))
    #ManyToOne => Sous categorie
    souscategories = db.relationship("souscategorie", backref="annonce", lazy="joined")
    souscategorie_id = db.Column(db.Integer, db.ForeignKey("souscategories.id"))
    #
    vendu = db.Column(db.Integer, nullable=True, default=0)
    promo = db.Column(db.Integer, nullable=True, default=0)
    nbreVue = db.Column(db.Integer, nullable=True, default=0)
    img = db.Column(db.Text(1000), nullable=True, default="/static/uploads/")
    date = db.Column(db.String(30), nullable=True)
    isArchived = db.Column(db.Integer,default=0)
    createBy = db.relationship("user", backref="annonce", lazy="joined")
    #ManyToOne => User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #ManyToOne => Categorie
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    categories = db.relationship("categorie", backref="annonce", lazy="joined")
    #OneToMany=> image
    images = db.relationship("image", backref="annonce", lazy="joined")
    #OneToMany=> favoris
    favoris = db.relationship("favoris", backref="annonce", lazy="joined")

    def  __init__(self,titre,description,prix,localite,date,categories,user,img="",vendu=0,nbreVue=0,isArchived=0):  
        self.titre = titre
        self.description = description
        self.img = img
        self.prix = prix    
        self.localite_id = localite
        self.categorie_id = categories
        self.date = date
        self.isArchived = isArchived
        self.nbreVue = nbreVue
        self.vendu = vendu
        self.user_id = user
    
    def __repr__(self) -> str:
        return "{}.{}".format(self.id,self.titre)
        
def getAll():
    return annonce.query.filter_by(isArchived=0,).order_by(annonce.id.desc()).all()

def getById(id):
    return annonce.query.filter_by(id=id,isArchived=0).first()

def getTenLatestAnnonces():
    return annonce.query.filter_by(isArchived=0).order_by(annonce.id.desc()).limit(10).all()

def getAnnonceByCategorieId(id):
    return annonce.query.filter_by(categorie_id=id, isArchived=0).order_by(annonce.id.desc()).all()

def getAnnonceByCreateBy(idUser):
    return annonce.query.filter_by(user_id=idUser, isArchived=0).order_by(annonce.id.desc()).all()

def getAnnoncesByCategorieId(idCategorie,idAnnonce):
    annonces = annonce.query.filter_by(categorie_id=idCategorie, isArchived=0).order_by(annonce.id.desc()).limit(5).all()
    for ann in annonces :
        if ann.id == idAnnonce:
            annonces.remove(ann)
    return annonces


def addView(id):
    ann = getById(id)
    ann.nbreVue += 1
    db.session.commit()

def searchLayout(objet="", lieu=""):
    if not objet.strip() and not lieu.strip():
        # Si aucun objet ni lieu n'est fourni, retourner toutes les annonces
        return getAll()
    elif not objet.strip() and lieu.strip():
        # Si seul le lieu est fourni, rechercher les annonces dans ce lieu
        return annonce.query.filter(annonce.localite_id == lieu).all()
    elif objet.strip() and not lieu.strip():
        # Si seul l'objet est fourni, rechercher les annonces contenant cet objet
        return annonce.query.filter(annonce.titre.like(f"%{objet}%")).all()
    return annonce.query.filter(annonce.titre.like(f"%{objet}%"), annonce.localite_id == lieu).all()


def searchBoutique(objet="", lieu="", categorie=""):
    if objet.strip() and lieu.strip() and categorie.strip():
        # Recherche avec objet, lieu et catégorie
        return annonce.query.filter(annonce.titre.like(f"%{objet}%"), annonce.localite_id == lieu, annonce.categorie_id == categorie).all()
    elif objet.strip() and lieu.strip():
        # Recherche avec objet et lieu
        return annonce.query.filter(annonce.titre.like(f"%{objet}%"), annonce.localite_id == lieu).all()
    elif objet.strip() and categorie.strip():
        # Recherche avec objet et catégorie
        return annonce.query.filter(annonce.titre.like(f"%{objet}%"), annonce.categorie_id == categorie).all()
    elif lieu.strip() and categorie.strip():
        # Recherche avec lieu et catégorie
        return annonce.query.filter(annonce.localite_id == lieu, annonce.categorie_id == categorie).all()
    elif objet.strip():
        # Recherche seulement avec objet
        return annonce.query.filter(annonce.titre.like(f"%{objet}%")).all()
    elif lieu.strip():
        # Recherche seulement avec lieu
        return annonce.query.filter(annonce.localite_id == lieu).all()
    elif categorie.strip():
        # Recherche seulement avec catégorie
        return annonce.query.filter(annonce.categorie_id == categorie).all()
    return annonce.query.all()
