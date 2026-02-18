from fastapi import APIRouter, status, HTTPException
from Tracker.database import db
from Tracker.Routes.Pydantic_Models import Category, CategoryUpdate

cat_router = APIRouter()


def response_format_cat(category):
    """
    This is a helper function to serialize a category
    :param category: dictionary with transaction info
    :return: Formatted print
    """
    return {
        "id": str(category["_id"]),
        "name": category["name"]
    }


@cat_router.post("/post_categories/", status_code=status.HTTP_201_CREATED,tags=["categories"])
def create_category(category: Category):
    """
    This is a post route to create a category
    :param category: new category
    :return: dict with formatted category
    """
    existing = db.cat_collection.find_one({"name": category.name})
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    result = db.create_category(category.model_dump())
    created = db.cat_collection.find_one({"_id": result.inserted_id})

    return response_format_cat(created)


@cat_router.get("/get_categories/",tags=["categories"])
def get_categories():
    """
    This is a get-route to get categories
    :return: All categories in formatted dict
    """
    categories = db.get_categories()
    return [response_format_cat(cat) for cat in categories]



@cat_router.patch("/categories/{name}",tags=["categories"])
def update_category(name: str, payload: CategoryUpdate):
    """
    This is update route to update a category
    :param name: name of the category
    :param payload:
    :return: formatted dict of updated category
    """

    update_data = payload.model_dump(exclude_unset=True)

    updated = db.update_category(name, update_data)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return response_format_cat(updated)



@cat_router.delete("/transactions/{name}",tags=["categories"])
def delete_category(name: str):
    """
    This is a delete route to delete a category
    :param name: name of the category
    :return: Message of deleted category
    """

    result = db.delete_category(name)

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {"message": "Category deleted successfully"}


