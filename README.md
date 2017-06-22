+--------------------------------------------------------------------------------------------------------+
|                                        Project 5: Item Catalog                                         |
+--------------------------------------------------------------------------------------------------------+
0. Introduction:
   This is a simple catalog item for specific google plus users. 
   If you want to add your own catalog, please login your google+ account.

1. How to run:
    a: open the command line(or terminal), direct to the folder where applicaiton.py is.
    b: run the server file by executing "python application.py . "in command line.
    c: browse the website in http://localhost:8080 or 127.0.0.1:8080

2. Structure:


                   |-- /catalog, /
                   |-- helper function: authentication(catalog_id, item_id)  
                   |-- helper function: reg(username, profile, email)
                   |-- /gconnect
                   |-- /gdisconnect
                   |-- /Item
                   |-- /login
    application.py-|-- /catalog/<int:catalog_id>/item, /catalog/<int:catalog_id>/
                   |-- /catalog/new
                   |-- /catalog/<int:catalog_id>/edit
                   |-- /catalog/<int:catalog_id>/delete
                   |-- /catalog/<int:catalog_id>/item/new
                   |-- /catalog/<int:catalog_id>/item/<int:item_id>/edit
                   |-- /catalog/<int:catalog_id>/item/<int:item_id>/delete
                   |-- /catalog/<int:catalog_id>/item/JSON
                   |-- /catalog/<int:catalog_id>/item/<int:item_id>/JSON




                    |- User-|-Id(int)
                    |       |-name(string(10))
                    |       |-profile(string(200))
                    |       |-email(string(50))
                    |      
                    |            |-Id(int)
    database.py-----|-Catagory --|-user_id(int)
                    |            |-name(string(50))
                    |            |
                    |-----------Item-|- Id(int)
                                     |- name(string(50))
                                     |- attribute(string(50))
                                     |- description(string(150))
                                     |- url_link(string(200))
                                     |- catagory_id(int, foreign_key)
                                     |- user_id(int, foreign_key)