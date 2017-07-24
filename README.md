## 					  Item Catalog

------

#### **Summary:**

- This is a simple catalog item for specific *google plus* users. Any improvements are welcomed. ​:smile:​
- ​You can browse all the items and categories of this catalog. You can use this catalog to store items(or other things that has a name) to different categories of your own. However, note that the categories you created **can be accessed by all people** ( and of course, me Alan, the author :blush: ).
- You also can obtain the XML and JSON format of single category or item. 
- The project utilizes Flask and SQLAlchemy for request handling and database administration.


- If you want to add/modify/delete your own catalog, please login your **google+** account.

#### How to run:

Please refer to the *Linux Server Configuration* [repo](https://github.com/yihuicai/Linux_Server_Configuration_FSND). **The project is no long runnable on local machine.**

~~a: Clone and pull this repository to your own computer~~

~~b: Open the Command Line Interface(or terminal), direct to the folder where `applicaiton.py` is.~~
~~c: Run the server file by executing`python database_setup.py` and `python application.py .` in command line. Make sure you have all the libraries on your own computer.~~
~~d: Browse the website in http://localhost:8080 or 127.0.0.1:8080~~

#### Routing Table:

*application.py*

|                 Handlers                 |                  Notes                   |
| :--------------------------------------: | :--------------------------------------: |
|               /catalog, /                | To render the front page that shows all catalogs and items |
|                /gconnect                 | To accept the authorization token from *Google+* |
|               /gdisconnect               |    To logout from a logged in account    |
|                  /login                  |         To render the login page         |
|               /catalog/new               | To add a new category (**authentication needed**) |
|      /catalog/<int:catalog_id>/edit      | To modify the name of a category (**authentication needed**) |
|     /catalog/<int:catalog_id>/delete     | To delete a category (**authentication needed**) |
| /catalog/<int:catalog_id>/item, /catalog/<int:catalog_id>/ |        To view a single category         |
| /catalog/<int:catalog_id>/item/<int:item_id> |     To view detailed info of an item     |
|    /catalog/<int:catalog_id>/item/new    | To add a new item to a category (**authentication needed**) |
| /catalog/<int:catalog_id>/item/<int:item_id>/edit | To edit an existing item (**authentication needed**) |
| /catalog/<int:catalog_id>/item/<int:item_id>/delete | To delete an existing item (**authentication needed**) |
|   /catalog/<int:catalog_id>/item/JSON    |  To obtain JSON endpoint of a category   |
| /catalog/<int:catalog_id>/item/<int:item_id>/JSON |    To obtain JSON endpoint of an item    |
|    /catalog/<int:catalog_id>/item/XML    |   To obtain XML endpoint of a category   |
| /catalog/<int:catalog_id>/item/<int:item_id>/XML |    To obtain XML endpoint of an item     |
