from os import path, listdir
from datetime import datetime
from lenskit_proxy import LenskitProxy
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    models = {}

    # # Get recommendations from data file or database
    # def get_recs(self, user_id, nr_recs, algo, items):
    #     dbManager = DbManager()
    #     ratings = dbManager.get_ratings()
    #     lkProxy = LenskitProxy()
    #     return lkProxy.get_recs(user_id, nr_recs, algo, ratings, items)
    
    # Get recommendations using a saved model
    def get_recs_using_model(self, user_id, nr_recs, algo, items):
        modelManager = ModelManager()
        lkProxy = LenskitProxy()
        dbManager = DbManager()
        model = Controller.models.get(algo, None)
        if model == None:
            print('\033[1;31;47m Model not loaded in memory!!! Model will be load now for this request. \033[0m')
            model = modelManager.load(algo)
        ratings = dbManager.get_ratings_for_user(user_id)
        ratings.set_index('item', inplace=True)
        #print(ratings.head())
        return lkProxy.get_recs_from_model(model, user_id, nr_recs, items, ratings)
    
    def get_model_info(self, algo):
        model_file_dir_path = "files/" + algo + '.pickle'
        creation_date = ""
        updated_date = ""
        size = 0
        if path.exists(model_file_dir_path):
            creation_date = datetime.utcfromtimestamp(path.getctime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S') 
            updated_date = datetime.utcfromtimestamp(path.getmtime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S')
            size = path.getsize(model_file_dir_path) / 1000
        return {"creation_date": creation_date + " UTC", "updated_date": updated_date + " UTC", "size": str(size) + " KB"}

    def upload_model(self, algo, file):
        file_name = path.join('files/' + algo + '.pickle')
        file.save(file_name)

    @staticmethod
    def preload_models():
        model_file_dir_path = "files/"
        modelManager = ModelManager()
        for filename in listdir(model_file_dir_path):
            if not filename.startswith('.'):
                key = filename.split('.')[0]
                Controller.models[key] = modelManager.load(filename)