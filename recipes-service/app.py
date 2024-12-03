from flask import Flask
from flask_cors import CORS
from models.recipe_model import RecipeModel
from services.recipe_services import RecipeService
from schemas.recipe_schemas import RecipeSchema
from routes.recipe_routes import RecipeRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)
db_conn_recipe = RecipeModel()
db_conn_recipe.connect_to_database()
recipe_service = RecipeService(db_conn_recipe)
recipe_schema = RecipeSchema()
recipe_routes = RecipeRoutes(recipe_service, recipe_schema)
app.register_blueprint(recipe_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn_recipe.close_connection()