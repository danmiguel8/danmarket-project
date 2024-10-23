from flask import session, redirect, url_for
from ..const.constantes import USER_CONNECTED, PANIER, TOTAL
from ..model import db 
from ..classes import categorie, annonce, localite, user
import datetime


#FONCTIONS
def categories():
    return categorie.getAll()

def localites():
    return localite.getAll()

def getDateActuelle():
    return datetime.datetime.now()

# def choiceOfRedirect(id,boutique):
#     if boutique is None:  
#         return redirect(f"/#{id}")
#     else:       
#         return redirect(f"/boutique#{id}")
    
def choiceOfRedirect(id,boutique=None,favorite=None,detail=None):
    if boutique is None and favorite is None and detail is None:  
        return redirect(f"/#{id}")
    if boutique != None or (favorite == "boutique" or detail == "boutique"):    
        return redirect(f"/boutique#{id}")
    if detail == "detail" and detail != None or (favorite == "detail" or boutique == "detail"):
        return redirect(f"/details/{id}")
    if favorite != None or (detail == "favorite" or boutique == "favorite"):
        return redirect(url_for('favorisRoute'))


def getUserConnected():
    user = ""
    if USER_CONNECTED in session :
        user = session.get(USER_CONNECTED)
    return user

def getElement(objet="error"):
    error = ""
    if objet in session :
        error = session.get(objet)
        session.pop(objet)
    return error

def getLen(objet):
    return len(session.get(objet,[]))

def getListOfAnnonce():
    result = []
    if PANIER in session:
        total = 0
        panier = session.get(PANIER, [])
        for id in panier:
            ann = annonce.getById(id)
            result.append(ann)
            total += ann.prix
        session[TOTAL] = total
    return result

def popPanierSession():
    if PANIER in session:
        session.pop(PANIER)
        if TOTAL in session:
            session.pop(TOTAL)

def turnToSold(id):
    ann = annonce.getById(id)
    ann.vendu = 1
    db.session.commit()

def getUserConnectedToAddToCreate():
    if USER_CONNECTED in session:
        return user.getById(getUserConnected()['id']) 
    return ""