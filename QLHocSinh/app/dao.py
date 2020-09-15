import hashlib
import json
import os
from app import app
from app.models import Teacher, AdminAll


def read_categories():
    with open(os.path.join(app.root_path, "data/categories.json"),
              encoding="utf-8") as f:
        return json.load(f)


def read_product_by_id(product_id):
    products = read_products()
    for p in products:
        if p["id"] == product_id:
            return p

    return None


def read_products(category_id=0, keyword=None, from_price=None, to_price=None):
    with open(os.path.join(app.root_path, "data/products.json"),
              encoding="utf-8") as f:
        products = json.load(f)

        if category_id > 0:
            products = [p for p in products if p["category_id"] == category_id]

        if keyword:
            products = [p for p in products if p["name"].lower().find(keyword.lower()) >= 0]

        # if from_price and to_price:
        #     products = [p for p in products if p["price"] >= float(from_price) and p["price"] <= float(to_price)]

        return products


def validate_user_teacher(username, password):
    hashpass = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = Teacher.query.filter(Teacher.userName == username.strip(),
                                Teacher.passWord == hashpass).first()
    if user:
        return user
    return None


def validate_user_admin(username, password):
    hashpass = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = AdminAll.query.filter(AdminAll.userName == username.strip(),
                                 AdminAll.passWord == hashpass).first()
    if user:
        return user
    return None


if __name__ == "__main__":
    print(read_products())
