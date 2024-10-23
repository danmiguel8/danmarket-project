import os
from ..model import app, save, mail
from ..classes import categorie, annonce, localite, user, favoris, vendu, image
from flask import render_template, request, session, flash, redirect, url_for
from ..const.constantes import *
from ..fonctions.functions import *
from passlib.hash import sha256_crypt
import stripe
from flask_mail import Message
public_key = "pk_test_oKhSR5nslBRnBZpjO6KuzZeX"
stripe.api_key = "sk_test_VePHdqKTYQjKNInc7u56JBrQ"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#ROUTES
@app.route("/")
def home():
    return render_template(PAGE_HOME, 
                            categories=categories(),
                            annonces=annonce.getTenLatestAnnonces(),
                            localites=localites(),
                            userconnected=getUserConnectedToAddToCreate(),
                            home = "",
                            nbre=getLen(PANIER)
                          )

@app.route("/boutique/", methods=['GET', 'POST'])
@app.route("/boutique/<int:id>", methods=['GET'])
def boutique(id=None):
    where = -1
    quoi = ""
    if request.method == 'POST':
        quoi = request.form['quoi']
        if 'boutique' in request.form :
            id = request.form['categorie']
            p = annonce.searchBoutique(request.form['quoi'], request.form['ou'], request.form['categorie'])
        elif 'layout' in request.form :
            p = annonce.searchLayout(request.form['quoi'], request.form['ou'])
        if request.form['ou'] != "":
            where = int(request.form['ou'])
    else:
        if id is not None:
            p = annonce.getAnnonceByCategorieId(id)
        else:
            p = annonce.getAll()
            id = -1
    return render_template(PAGE_BOUTIQUE, annonces = p,
                                          categories = categories(),
                                          selectedCategorie = id,
                                          localites=localites(),
                                          selectedLocalite=where,
                                          objetCherche = quoi,
                                          userconnected = getUserConnectedToAddToCreate(),
                                          home = "boutique",
                                          nbre=getLen(PANIER)
                          )

@app.route("/favoris/")
@app.route("/favoris/<int:id>/")
@app.route("/favoris/<int:id>/<boutique>")
@app.route("/favoris/<int:id>/<favorite>")
@app.route("/favoris/<int:id>/<detail>")
def favorisRoute(id=None,boutique=None,favorite=None,detail=None):
    if USER_CONNECTED in session:
        userconnected = getUserConnectedToAddToCreate()
        if id is None:
            favs = favoris.getFavorisByUser(userconnected.id)
            return render_template(PAGE_FAVORIS,
                                   userconnected = userconnected,
                                   annonces = favs,
                                   home = "favorite",
                                   localites=localites(),
                                   nbre=getLen(PANIER)
                                   )
        else:
            # fav = favoris.favoris(userconnected["id"], id)
            favoris.updateOrInsertByUserAndAnnonce(userconnected.id, id)
            return choiceOfRedirect(id,boutique,favorite,detail)
    else:
        flash("Vous devez vous connecter pour ajouter une annonce aux favoris.", "error")
        return choiceOfRedirect(id,boutique,favorite,detail)


@app.route("/connexion", methods=['GET', 'POST'])
def connexion():
    if request.method == "POST":
        us = user.getUserByLoginAndPassword(request.form["login"],request.form["password"])
        if us is None:
            session["error"] = "Login et/ou Mot de passe incorrect !"
            return redirect(url_for('connexion'))
        else:
            session[USER_CONNECTED] = us.toJson()
            return redirect(url_for('home'))
    else :
        return render_template(PAGE_CONNEXION,
                               error=getElement(),
                               userconnected=getUserConnectedToAddToCreate(),
                               nbre=getLen(PANIER)
                              )

@app.route("/deconnexion")
def deconnexion():
    if USER_CONNECTED in session:
        session.pop(USER_CONNECTED)
        popPanierSession()
    return redirect(url_for('home'))

@app.route("/panier/")
@app.route("/panier/<page>/")
@app.route("/panier/<int:id>/")
@app.route("/panier/<int:id>/<boutique>")
@app.route("/panier/<int:id>/<favorite>")
@app.route("/panier/<int:id>/<detail>")
def panier(id=None,boutique=None,favorite=None,page=None,detail=None):
    if page is None :
        if id is not None:
            if USER_CONNECTED in session:
                panier = session.get(PANIER, [])  # Récupère la liste du panier ou une liste vide si elle n'existe pas
                if id not in panier:
                    panier.append(id)  # Ajoute l'ID au panier
                session[PANIER] = panier  # Met à jour la session avec la liste mise à jour
            else:
                flash("Vous devez vous connecter pour ajouter à votre panier.", "error")
        else:
            panier = session.get(PANIER, [])  # Récupère la liste du panier ou une liste vide si elle n'existe pas
        return choiceOfRedirect(id,boutique,favorite,detail)
    else:
        # print("Contenu de la session du panier:", session.get(PANIER, []))
        # print("Longueur du panier:", len(session.get(PANIER, [])))
        nbre = 0 
        total = 0
        panier = getListOfAnnonce()
        if PANIER in session :
            nbre = len(session.get(PANIER, []))
            total = session.get(TOTAL)
        return render_template(PAGE_PANIER,
                                panier=panier,
                                nbre=nbre,
                                total=total,
                                public_key=public_key,
                                logo = LOGO,
                                userconnected=getUserConnectedToAddToCreate()
                              )

@app.route("/inscription", methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nomComplet = request.form["nomComplet"]
        login = request.form["login"]
        password = request.form["password"]
        if user.getUserByLogin(login) is None:
            save(user.user(login,sha256_crypt.encrypt(password),nomComplet,CLIENT,0))
            flash("Inscription terminé avec succes.", "error")
            return redirect(url_for('home'))
        else:
            session["error"] = "Echec de la création du compte, Login/Email déjà existant!"
            session["nomComplet"] = nomComplet
            return redirect(url_for('inscription'))
    return render_template(PAGE_INSCRIPTION,
                            nbre=getLen(PANIER),
                            error = getElement(),
                            nomComplet = getElement("nomComplet"),
                            userconnected=getUserConnectedToAddToCreate()
                          )

@app.route("/paiement", methods=['POST'])
def paiement(id=None):
    typeTarif = ""
    if "typeTarif" in request.form:
        typeTarif = request.form["typeTarif"]
    if typeTarif == "":
        customer = stripe.Customer.create(email=request.form['stripeEmail'], source= request.form['stripeToken'])
        charge = stripe.PaymentIntent.create(
            customer=customer.id,
            amount=int(session.get(TOTAL)),
            currency="xof",
            description="paiement"
        )

        if PANIER in session:
            panier = session.get(PANIER, [])
            for id in panier:
                turnToSold(id)
                save(vendu.vendu(getUserConnected()['id'],id))
            popPanierSession()
            flash("Votre commande a bien été réglée!!",'succesPanier')
        return redirect("/panier/<page>/")  
    else:  
        if USER_CONNECTED not in session:
            return redirect(url_for('connexion'))
        else:
            userconnected = getUserConnected()['id']
            user.addAbonnementToUser(userconnected,typeTarif)
        return redirect(url_for('home'))

@app.route("/details/<int:id>/")
@app.route("/details/<int:id>/<me>")
def details(id,me=None):
    ann = annonce.getById(id)
    similaire = annonce.getAnnoncesByCategorieId(ann.categorie_id,ann.id)
    if me == None:
        #return f"{image.getImagesByAnnonceId(ann.id)}"
        annonce.addView(id)
        me = "ok"
    else:
        me = "no"
    return render_template(PAGE_DETAIL_ARTICLE,
                           nbre=getLen(PANIER),
                           annonce = ann,
                           images = image.getImagesByAnnonceId(id),
                           home = "detail",
                           like = len(favoris.getAnnonceFavoriteById(id)),
                           logo = LOGO,
                           userconnected=getUserConnectedToAddToCreate(),
                           similaire = similaire,
                           voir = me
                          )

@app.route("/retirer/<int:id>")
def retirer(id):
    if USER_CONNECTED in session:
        if id is not None:
            panier = session.get(PANIER, [])  # Récupère la liste du panier ou une liste vide si elle n'existe pas
            if id in panier:
                panier.remove(id) 
            session[PANIER] = panier 
            if len(panier)<1:
               session.pop(PANIER)
            return redirect("/panier/page")  
    return redirect(url_for("home"))
    
@app.route("/compte")
def compte():
    if USER_CONNECTED in session:
        return render_template(PAGE_COMPTE,
                                userconnected=getUserConnectedToAddToCreate(),
                                nbre=getLen(PANIER)
                               )
    return redirect(url_for('connexion'))

#PAS ENCORE UTILISÉ
@app.route("/promotion")
def promotion():
    return "promotion"

@app.route("/apropos")
def apropos():
    return "apropos"

@app.route("/tarif")
def tarif():
    return render_template(PAGE_TARIF,
                           userconnected=getUserConnectedToAddToCreate(),
                           nbre=getLen(PANIER),
                           logo = LOGO,
                           public_key=public_key
                           )

@app.route("/contact")
def contact():
    return render_template(PAGE_CONTACT,
                           userconnected=getUserConnectedToAddToCreate(),
                           nbre=getLen(PANIER),
                           )

@app.route("/sendmail",methods=['POST'])
def sendmail():
    nomComplet = request.form["name"]
    email = request.form["email"]
    comment = request.form["comment"]
    msg = Message('Contact pour support', sender = email, recipients = ['support@danmarket.sn'])
    msg.body = f"Nom et Prenom : {nomComplet}\nObjet : {comment}"
    mail.send(msg)
    flash("Votre message a bien été envoyé!.", "msg")
    return redirect(url_for('contact'))


@app.route("/publierannonce", methods=['GET', 'POST'])
def publierannonce():
    if request.method == "POST":
        if USER_CONNECTED not in session:
            return redirect(url_for('connexion'))
        userconnected = getUserConnectedToAddToCreate()
        if userconnected.premium == 0:
            flash('Aucun abonnement trouvé!','errorAbonnement')
            return  redirect(url_for("publierannonce"))
        titre = request.form['titre']
        filename= ""
        nbreAnnonce = len(annonce.getAll())
        # return f"{userconnected.premium} - {userconnected.typePremium}"
        if 'imagePrincipale' in request.files:
            file = request.files['imagePrincipale']
            if file.filename != '':
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{timestamp}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        newAnnonce = annonce.annonce(titre,
                                     request.form['description'],
                                     request.form['prix'],
                                     int(request.form['localite']),
                                     str(getDateActuelle()),
                                     int(request.form['categorie']),
                                     int(userconnected.id),
                                     str(f"/static/uploads/{filename}")
                                     ) 
        
        nbreImages = 3

        if userconnected.typePremium == PREMIUM:
            nbreImages = 10
        if userconnected.typePremium == PREMIUM_PLUS:
            nbreImages = 15
        j = 1
        for i in range(len(request.files.getlist('imageSecondaires'))):
            if j <= nbreImages:
                img = request.files.getlist("imageSecondaires")[i]
                if img.filename != "":
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f"{timestamp}_{img.filename}"
                    img.save(os.path.join(UPLOAD_FOLDER, filename))
                    save(image.image(f"/static/uploads/{filename}", nbreAnnonce+1))
                j+=1
        save(newAnnonce)
        return redirect(url_for('mesannonces'))
    return render_template(PAGE_PUBLIER_ANNONCE,
                           userconnected=getUserConnectedToAddToCreate(),
                           nbre=getLen(PANIER),
                           categories=categorie.getAll(),
                           localites=localite.getAll(),
                           error=getElement()
                           )

#VENTES / ARTICLES / GESTIONNAIRE

@app.route("/gestionnaire")
def gestionnaire():
    userconnected = getUserConnectedToAddToCreate()
    if userconnected != "" :
        vendus = vendu.getAll()
        ventes = []
        for v in vendus:
            article = annonce.getById(v.annonce_id)
            if article.user_id == userconnected.id :
                ventes.append(article)
        articles = annonce.getAnnonceByCreateBy(userconnected.id)
        return render_template(PAGE_GESTION,
                               nbre=getLen(PANIER),
                               nbreArticles = len(articles),
                               nbreVentes = len(ventes),
                               logo = LOGO,
                               userconnected=getUserConnectedToAddToCreate(),
                               )
    return redirect(url_for('home'))

@app.route("/mesventes")
def mesventes():
    userconnected = getUserConnectedToAddToCreate()
    if userconnected != "" :
        vendus = vendu.getAll()
        articles = []
        for v in vendus:
            article = annonce.getById(v.annonce_id)
            if article.user_id == userconnected.id :
                articles.append(article)
        return render_template(PAGE_MIXTE_ACHAT_VENTE_ANNONCE_OF_CLIENT,
                               nbre=getLen(PANIER),
                               articles = articles,
                               nbreArticle = len(articles),
                               logo = LOGO,
                               userconnected = getUserConnectedToAddToCreate(),
                               localites = localites(),
                               texte = "ARTICLES VENDUS"
                               )
    return redirect(url_for('home'))

@app.route("/mesachats")
def mesachats():
    userconnected = getUserConnectedToAddToCreate()
    if userconnected != "" :
        vendus = vendu.getAnnonceByUserId(userconnected.id)
        articles = []
        for v in vendus:
            articles.append(annonce.getById(v.annonce_id)) 
        return render_template(PAGE_MIXTE_ACHAT_VENTE_ANNONCE_OF_CLIENT,
                               nbre = getLen(PANIER),
                               articles = articles,
                               logo = LOGO,
                               userconnected = getUserConnectedToAddToCreate(),
                               localites = localites(),
                               texte = "ACHATS EFFECTUÉS"
                               )
    return redirect(url_for('home'))

@app.route("/mesannonces")
def mesannonces():
    userconnected = getUserConnectedToAddToCreate()
    if userconnected != "" :
        articles = annonce.getAnnonceByCreateBy(userconnected.id)
        return render_template(PAGE_MIXTE_ACHAT_VENTE_ANNONCE_OF_CLIENT,
                               nbre = getLen(PANIER),
                               articles = articles,
                               nbreArticle = len(articles),
                               logo = LOGO,
                               userconnected=getUserConnectedToAddToCreate(),
                               localites = localites(),
                               texte = "ANNONCES PUBLIÉES"
                               )
    return redirect(url_for('home'))