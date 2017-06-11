from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def All_catalog():
    return "Page: All_catalog"
    
@app.route('/catalog/<int:catalog_id>/new')
def New_catalog(catalog_id):
    return "Page: %s New_catalog"%catalog_id

@app.route('/catalog/<int:catalog_id>/edit')
def Edit_catalog(catalog_id):
    return "Page: %sEdit_catalog"%catalog_id
    
@app.route('/catalog/<int:catalog_id>/delete')
def Delete_catalog(catalog_id):
    return "Page: %sDelete_catalog"%catalog_id
    
@app.route('/catalog/<int:catalog_id>/item')
def All_items(catalog_id):
    return "Page: %s, All_items"%catalog_id
    
@app.route('/catalog/<int:catalog_id>/item/new')
def New_item(catalog_id):
    return "Page: %sNew_items"%catalog_id

@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/edit')
def Edit_item(catalog_id, item_id):
    return "Page: Edit_item%s"%item_id
    
@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/delete')
def Delete_item(catalog_id, item_id):
    return "Page: Delete_item%s"%item_id

if __name__=='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080)