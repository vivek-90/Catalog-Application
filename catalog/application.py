from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    jsonify)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from Database_setup import Base, Category, Item, User
from flask import session as login_session
import random,string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Web client 1"


engine = create_engine('sqlite:///catalogwithusers1.db')
Base.metadata.bind = engine

DBSession =sessionmaker(bind=engine)
session = scoped_session(DBSession)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) 
        for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = json.loads(answer.text)
    

    login_session['username'] = '  '
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


    user_id =getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome!'
    output += login_session['username']
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;' \
                'height: 300px;'\
                'border-radius: 150px;'\
                '-webkit-border-radius: 150px;'\
                '-moz-border-radius: 150px;">'
    print "done!"
    return output

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None    


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response    


@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(category=[i.serialize for i in items])

@app.route('/category/<int:category_id>/<int:item_id>/JSON')
def ItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id= item_id).one()
    return jsonify(item=item.serialize)

# Task 1: Create route for category function here
@app.route('/')
@app.route('/category/')
def categoryall():
    category = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('publiccatalog.html', category = category)
    else:
        return render_template('categories.html', category = category)    

    

# Task 2: Create route for Item function here
@app.route('/category/<int:category_id>/')
def showitem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return render_template('items.html', category = category, items = items)


# Task 3: Create route for Item Descrpition function here
@app.route('/category/<int:category_id>/<int:item_id>/description/')
def showdescription(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(id=item_id).one()
    if 'email' not in login_session:
        return render_template(
            'publicdescription.html', 
            category = category, 
            items = items, 
            creator= creator
        )
    else:
        return render_template(
            'description.html', 
            items=items, 
            category=category, 
            creator=creator
        )


# Task 4: Create route for newItem function here
@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    if 'email' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newIt = Item(
            name = request.form['name'], 
            description = request.form['description'], 
            category_id = category_id, 
            user_id=login_session['user_id']
        )
        session.add(newIt)
        session.commit()
        return redirect(url_for('categoryall', category_id = category_id)) 
    else:
        return render_template('newitem.html', category_id = category_id)

# Task 5: Create route for editItem function here
@app.route('/category/<int:category_id>/<int:item_id>/edit/', methods = ['GET','POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if 'email' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorised to Edit this item. \
        Please create your own item in order to Edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showitem', category_id=category_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editItem.html', 
            category_id=category_id, 
            item_id=item_id, 
            item=editedItem
        )


# Task 6: Create a route for deleteItem function here
@app.route('/category/<int:category_id>/<int:item_id>/delete/', methods =['GET','POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if 'email' not in login_session:
        return redirect('/login')    
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() \
        {alert('You are not authorised to delete this item. \
        Please create your own item in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('categoryall'))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)