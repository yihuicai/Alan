from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catagory, Item, User

#for authentication
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from flask import make_response
import requests
import random
import string

CLIENT_ID=json.loads(open('client_secrets.json','r').read())['web']['client_id']
app = Flask(__name__)
engine=create_engine('sqlite:///catalog.db')
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
status={'username' : 'guest', 'profile' : 'http://megaconorlando.com/wp-content/uploads/guess-who.jpg', 'id' : -1}

def reg(username, profile, email):
    try:
        u=session.query(User).filter_by(email=email).one()
    except: 
        newuser=User(name=username, email=email, profile=profile)
        session.add(newuser)
        session.commit()
        u=session.query(User).filter_by(email=email).one()
    return u.Id


def authentication(catalog_id, item_id):
    def decorated(f):
        if status['username']=='guest':
            flash('Please login first')
            return redirect(url_for('showLogin'))
        else:
            if catalog_id:
                cata=session.query(Catagory).filter_by(Id=catalog_id).one()
                if status['id']== cata.user_id:
                    return f(status['id'], catalog_id, item_id)
                else:
                    flash('User not permitted to this action')
                    return redirect(url_for('All_catalog'))
            else: 
                return f(status['id'], catalog_id, item_id)
            
            
    return decorated

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response=make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type']='application/json'
        return response
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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'%access_token)
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

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id']=gplus_id


    email = data['email']
    status['username'] = data['name']
    status['profile'] = data['picture']
    status['id'] = reg(status['username'], status['profile'], email)
    

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'%login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    status['username']='guest'
    status['profile']='http://megaconorlando.com/wp-content/uploads/guess-who.jpg'
    status['id']=-1
    if result['status'] == '200':
	del login_session['access_token'] 
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'

    	return response
    else:
	
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

@app.route('/catalog/<int:catalog_id>/item/<int:item_id>')
def Items(catalog_id, item_id):
    item=session.query(Item).filter_by(Id=item_id).one()
    catalog=session.query(Catagory).filter_by(Id=catalog_id).one()
    return render_template('item.html', item=item, catalog=catalog)

@app.route('/login')
def showLogin():
    if not status['username']=='guest':
            flash('User already login, please logout first.')
            return redirect(url_for('All_catalog'))
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html',state=state)
    
@app.route('/')
@app.route('/catalog')
def All_catalog():
    catalog= session.query(Catagory).all()
    catagory=[]
    latest=session.query(Item).from_statement(text("SELECT * FROM Item ORDER BY Id DESC LIMIT 2")).all()
    for i in catalog:
        cata_item={}
        cata_item['id']=i.Id
        cata_item['name']=i.name
        cata_item['user_id']=i.user_id
        items= session.query(Item).filter_by(catagory_id=i.Id).all()
        cata_item['items']=items
        catagory.append(cata_item)
    return render_template('all_catalog.html',catalog=catagory,latest=latest,status=status,)

@app.route('/catalog/<int:catalog_id>')
@app.route('/catalog/<int:catalog_id>/item')
def This_catalog(catalog_id):
    catagory=[]
    catalog= session.query(Catagory).filter_by(Id=catalog_id).one()
    cata_item={}
    cata_item['id']=catalog.Id
    cata_item['name']=catalog.name
    cata_item['user_id']=catalog.user_id
    items=session.query(Item).filter_by(catagory_id=catalog.Id).all()
    cata_item['items']=items
    catagory.append(cata_item)
    return render_template('all_catalog.html',catalog=catagory,latest=[],status=status)

@app.route('/catalog/new', methods=['GET','POST'])
def New_catalog():
    @authentication(catalog_id=None, item_id=None)
    def dec_newC(user_id, catalog_id, item_id):
        if request.method == 'GET':
            return render_template('new_catalog.html')
        else:
            if request.form['name']:
                newCatagory=Catagory(name=request.form['name'], user_id=user_id)
                session.add(newCatagory)
                flash("New catagory created!")
                session.commit()
                return redirect(url_for('All_catalog'))
            else:
                flash("Please give a name for catagory")
                return render_template('new_catalog.html')
    return dec_newC
    
@app.route('/catalog/<int:catalog_id>/edit', methods=['Get', 'Post'])
def Edit_catalog(catalog_id):
    @authentication(catalog_id, item_id=None)
    def dec_editC(user_id, catalog_id, item_id):
        catagory=session.query(Catagory).filter_by(Id=catalog_id).one()
        if request.method == 'GET':
            return render_template('edit_catalog.html',catagory=catagory)
        else:
            if request.form['name']:
                catagory.name=request.form['name']
                session.add(catagory)
                flash("Catagory modified!")
                session.commit()
                return redirect(url_for('This_catalog', catalog_id=catalog_id))
            else:
                flash("Please give a name to edit the catagory.")
                return render_template('edit_catalog.html',catagory=catagory)
    
    return dec_editC

@app.route('/catalog/<int:catalog_id>/delete', methods=['GET','POST'])
def Delete_catalog(catalog_id):
    @authentication(catalog_id, item_id=None)
    def dec_deleteC(user_id, catalog_id, item_id):
        catagory=session.query(Catagory).filter_by(Id=catalog_id).one()
        if request.method == 'GET':
            return render_template('delete_catalog.html',catagory=catagory)
        else:
            item=session.query(Item).filter_by(catagory_id=catalog_id).all()
            session.delete(catagory)
            if item:
                for i in item:
                    session.delete(i)
            flash("Catagory and its items deleted!")
            session.commit()
            return redirect(url_for('All_catalog'))
    return dec_deleteC

@app.route('/catalog/<int:catalog_id>/item/new',  methods=['GET','POST'])
def New_item(catalog_id):
    @authentication(catalog_id, item_id=None)
    def dec_newI(user_id, catalog_id, item_id):
        if request.method == 'GET':
            return render_template('new_item.html', catalog_id=catalog_id)
        else:
            if request.form['name']:
                newItem=Item(name=request.form['name'], attribute=request.form['attribute'],
                description=request.form['description'], url_link=request.form['url'], catagory_id=catalog_id, user_id=user_id)
                session.add(newItem)
                flash("An item has been created!")
                session.commit()
                return redirect(url_for('This_catalog', catalog_id=catalog_id))
            else:
                flash("Please give a name for item")
                return redirect(url_for('All_catalog'))
    return dec_newI

@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/edit',  methods=['GET','POST'])
def Edit_item(catalog_id, item_id):
    @authentication(catalog_id, item_id)
    def dec_editI(user_id, catalog_id, item_id):
        item=session.query(Item).filter_by(Id=item_id).one()
        if request.method == 'GET':
            return render_template('edit_item.html', catalog_id=catalog_id, item=item)
        else:
            if request.form['name']:
                item.name=request.form['name']
                item.attribute=request.form['attribute']
                item.description=request.form['description']
                item.url_link=request.form['url']
                session.add(item)
                flash("An item has been edited!")
                session.commit()
                return redirect(url_for('This_catalog', catalog_id=catalog_id))
            else:
                flash("Please give a name to the edited item.")
                return render_template('edit_item.html', catalog_id=catalog_id, item=item)
    return dec_editI
            
@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/delete',  methods=['GET','POST'])
def Delete_item(catalog_id, item_id):
    @authentication(catalog_id, item_id)
    def dec_deleteI(user_id, catalog_id, item_id):
        item=session.query(Item).filter_by(Id=item_id).one()
        if request.method == 'GET':
            return render_template('delete_item.html',catalog_id=catalog_id, item=item)
        else:
            session.delete(item)
            flash("An item has been deleted!")
            session.commit()
            return redirect(url_for('This_catalog',catalog_id=catalog_id))
    return dec_deleteI
        
if __name__=='__main__':
    app.secret_key='Alan\'s Key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)