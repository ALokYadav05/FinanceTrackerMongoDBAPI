from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import datetime
import os


load_dotenv()


class Database:
    def __init__(self):
        """
         constructor sets up the connection to the database and creates two-collections
        """
        try:
            self.client = MongoClient(os.getenv("CONNECTION_URL"))
            self.db = self.client["Tracker"]
            self.transactions = self.db["transactions"]
            self.categories = self.db["categories"]
            print("Database budget created successfully")
        except Exception as e:
            print(f"Failed to connect to database: {e}")


    def createTransaction(self, data):
        """
        This method creates a transaction record in the database
        :param data: Dict of transaction
        :return: data created in database
        Note: here, we are inserting new field db , created_at
        """
        data["created_at"] = datetime.datetime.now()
        self.transactions.insert_one(data)
        return data


    def getAllTransactions(self,page_size=5):
        """
        This method gets all the transactions in the database
        :param page_size : used to limit the number of transactions to display
        :return: all the data from database
        """
        data = self.transactions.find().limit(page_size)
        return data


    def getTransactionById(self,transaction_id):
        """
        This method gets a single transaction record in the database using id
        :param transaction_id:
        :return: the extracted data from database
        """
        single_data = self.transactions.find_one({"_id": ObjectId(transaction_id)})
        if single_data:
            return single_data
        else:
            return f"No-Transaction found with this : {transaction_id} ID"


    def deleteTransaction(self,transaction_id):
        """
        This method deletes a transaction record in the database using id
        :param transaction_id:
        """
        record_found = self.transactions.find_one({"_id":ObjectId(transaction_id)})
        if record_found:
            self.transactions.delete_one({"_id": ObjectId(transaction_id)})
            return {'message':"Successfully deleted transaction"}
        else:
            return {'Error' :"Failed to delete transaction"}


    def deleteManyTransaction(self,category:str):
        """
        This method deletes multiple transactions in the database
        :param category: str
        :return: Dictionary of transactions deleted
        """
        new_category = category.lower()
        return self.transactions.delete_many({"category":new_category})


    def updateTransaction(self,transaction_id:str,updated_data:dict):
        """
        This method updates a transaction record in the database
        :param transaction_id: str
        :param updated_data: dictionary
        :return:
        """
        updated_data["updated_at"] = datetime.datetime.now()
        result = self.transactions.update_one({"_id": ObjectId(transaction_id)},{"$set":updated_data})
        if result.matched_count == 0:
            return None
        return self.transactions.find_one({"_id": ObjectId(transaction_id)})


    def searchTransactions(self,query:str):
        """
        This method searches for transactions in the database using specific attribute (query)
        :param query: str
        :return: list of transactions found
        """
        search_filter = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }
        return list(self.transactions.find(search_filter))


    def update_category(self,name:str,updated_data:dict):
        """
        This method updates a category record in the database
        :param name: str
        :param updated_data:
        :return: None or the updated collection
        """
        updated_data["updated_at"] = datetime.datetime.now()
        category = self.categories.find_one({"name": name})
        if not category:
            return None

        self.categories.update_one(
            {"_id": category["_id"]},
            {"$set": updated_data}
        )
        return self.categories.find_one({"_id": category["_id"]})


    def delete_category(self,name:str):
        """
        This method deletes a category record in the database
        :param name: str
        :return: the deleted record in the category collection
        """
        return self.categories.delete_one({"name":name})


db = Database()  # global-instance