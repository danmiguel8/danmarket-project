from .routeclient import app
from ..model import db 
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, render_template, request
from ..const.constantes import *
from ..fonctions.functions import *
from ..classes import user as User
from ..classes import annonce as Annonce
from ..classes import categorie as Categorie
from ..classes import localite as Localite
from ..classes import vendu as Vendu
from passlib.hash import sha256_crypt
from ..fonctions.functions import *

from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join

from src.classes.categorie import categorie
from src.classes.user import user
from src.classes.annonce import annonce
from src.classes.souscategorie import souscategorie
from src.classes.localite import localite
from src.classes.motcles import motcles
from src.classes.image import image
  
    
class MyAdminView(AdminIndexView):
    @expose("/")
    def index(self):
        if USER_CONNECTED not in session:
            return redirect(url_for('loginAdmin'))
        userc = getUserConnected()
        if(userc['role'] != ADMIN):
            return render_template(PAGE_403)
        articles = Annonce.getAll()
        categories = Categorie.getAll()
        users = User.getAll()
        localites = Localite.getAll()
        vendus = Vendu.getAll()
        return self.render('admin/index.html', 
                            userconnected=userc['nomCompet'], 
                            logo=LOGO,
                            articles=len(articles),
                            categories=len(categories),
                            users=len(users),
                            localites=len(localites),
                            vendus=len(vendus)
                           )

class UserView(ModelView):
    form_columns =["nomComplet","login","password","role"]
    create_modal = False
    page_size = 3

    column_display_pk = True

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    # 
    def is_accessible(self):
        if USER_CONNECTED not in session:
            return False
        return True
        
    def inaccessible_callback(self, name, **kwargs):
        return "Connectez-vous!"
    
    def on_model_change(self, form, model, is_created):
        model.password = sha256_crypt.encrypt(model.password)

class AnnonceView(ModelView):
    column_list = ("id","titre","description","prix","prixpromo","localites","date","createBy","categories","souscategories","nbreVue","isArchived")
    form_columns = ["titre","description","prix","prixpromo","localites","img","categories","souscategories"]
    create_modal = False
    page_size = 3

    column_display_pk = True

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True

    def on_model_change(self, form, model, is_created):
        model.createBy = getUserConnectedToAddToCreate()
        model.date = getDateActuelle()
        model.nbreVue = 0

class CategorieView(ModelView):
    column_list = ("id","libelle","createBy","isArchived")
    form_columns = ["libelle","img","isArchived"]
    create_modal = False
    page_size = 3

    column_display_pk = True

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True

    def on_model_change(self, form, model, is_created):
        model.createBy = getUserConnectedToAddToCreate()
    

class ImageView(ModelView):
    column_list = ("id","annonces","isArchived")
    form_columns = ["img","annonces","isArchived"]
    create_modal = False
    page_size = 3

    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True

class SousCategorieView(ModelView):
    column_list = ("id","libelle","categories","createBy","isArchived")
    form_columns = ["libelle","categories","isArchived"]
    create_modal = False
    page_size = 3

    def on_model_change(self, form, model, is_created):
        model.createBy = getUserConnectedToAddToCreate()

    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True

class LocaliteView(ModelView):
    column_list = ("id","libelle","isArchived")
    form_columns = ["libelle","isArchived"]
    create_modal = False
    page_size = 3

    def on_model_change(self, form, model, is_created):
        model.createBy = getUserConnectedToAddToCreate()

    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True

admin = Admin(app,name = "DANMARKET",template_mode="bootstrap4", index_view=MyAdminView(name=("Accueil")))


admin.add_view(UserView(user, db.session)) 
admin.add_view(AnnonceView(annonce, db.session))
admin.add_view(ImageView(image, db.session))
admin.add_view(CategorieView(categorie, db.session))
admin.add_view(SousCategorieView(souscategorie, db.session))
admin.add_view(LocaliteView(localite, db.session))
admin.add_view(ModelView(motcles, db.session))
admin.add_view(FileAdmin(UPLOAD_FOLDER,'/uploads/',name="Uploads"))


@app.route("/admin/login", methods=['GET', 'POST'])
def loginAdmin():
    if request.method == "POST":  
        us = User.getUserByLoginAndPassword(request.form["login"],request.form["password"])
        if us is None:
            return render_template(PAGE_403)
        else:
            if us.role != ADMIN :
                return render_template(PAGE_403)
            if USER_CONNECTED not in session:
                session[USER_CONNECTED] = us.toJson()
            return redirect('/admin')
    else:
        # if USER_CONNECTED in session:
        #     if getUserConnected()['role'] != ADMIN:
        #         return render_template(PAGE_403)
        #     return redirect('/admin')
        return render_template(PAGE_LOGIN_ADMIN,error=getElement()) 

@app.route("/admin/logout")
def logoutAdmin():
    if USER_CONNECTED in session:
        session.pop(USER_CONNECTED)
    return redirect(url_for('loginAdmin'))
