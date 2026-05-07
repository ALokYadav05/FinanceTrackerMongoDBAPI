from fastapi import APIRouter, status, HTTPException, Query
from Tracker.Routes.Pydantic_Models import TransactionCreate ,TransactionUpdate
from Tracker.database import db

trans_router = APIRouter()

def response_format_trans(transaction):
    """
     It is a  helper function to format  the response of transaction
    :param transaction: dict with transaction details
    :return: Formatted response
    """
    return {
        "id": str(transaction["_id"]),
        "title": transaction["title"],
        "description": transaction["description"],
        "amount": transaction["amount"],
        "type": transaction["type"],
        "category": transaction["category"],
        "date": transaction["date"],
        "tags": transaction["tags"],
    }


@trans_router.post("/",status_code=status.HTTP_201_CREATED)
def create_transaction(transaction:TransactionCreate):
    try:
        trans = transaction.model_dump(mode="json")
        created_transaction = db.createTransaction(trans)
        return response_format_trans(created_transaction)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@trans_router.get("/search",status_code=status.HTTP_200_OK)
def search_transactions(query:str):
    """
    This is a Get-router for searching transactions
    :param query: To search with title or description
    :return: formatted dict
    """
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Missing Search query")
    results = db.searchTransactions(query)
    transactions = [response_format_trans(t) for t in results]

    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No matching transaction not found")
    return transactions


@trans_router.get("/",status_code=status.HTTP_200_OK)
def get_transactions(page_size:int=Query(10,le=100)):
    """
    This is a Get-router for searching all transactions
    :param page_size: default-10
    :return: transaction in formatted dict
    """
    transactions = db.getAllTransactions(page_size)
    return [response_format_trans(t) for t in transactions]


@trans_router.get("/{id}",status_code=status.HTTP_200_OK)
def get_transaction(id_:str):
    """
    This is a Get-router for searching specific transactions by id
    :param id_: transaction id
    :return: formatted dict
    """
    try:
        transaction = db.getTransactionById(id_)
        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Transaction not found")
        return response_format_trans(transaction)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid transaction ID")



@trans_router.delete("/{id}",status_code=status.HTTP_200_OK)
def delete_transaction(id_:str):
    """
    This route is for deleting a transaction.
    :param id_: transaction id
    :return: deleted transaction
    """
    try:
        res = db.deleteTransaction(id_)
        return res
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid transaction ID")


@trans_router.delete("/bulk/{category}",status_code=status.HTTP_202_ACCEPTED)
def bulk_delete_transaction(category:str):
    """
    This route is for deleting a bulk transaction at a time
    :param category:
    :return: message in dict-format
    """
    result = db.deleteManyTransaction(category)
    if result:
        return{
            "message":"Transaction deleted successfully",
            "deleted_count": result.deleted_count,
        }
    else:
        return {"Message":"Transaction could not be deleted"}


@trans_router.patch("/{id}",status_code=status.HTTP_200_OK)
def update_transaction(id_:str,payload:TransactionUpdate):
    """
    This route is for updating a transaction
    :param id_:
    :param payload: pydantic-object
    :return: Formated-response
    """
    try:
        updated_transaction = db.updateTransaction(id_,payload.model_dump(exclude_unset=True))
        if not updated_transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Transaction not found")
        return response_format_trans(updated_transaction)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid transaction ID")
