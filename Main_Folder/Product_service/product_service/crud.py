from sqlmodel import Session, select
from .models import Product

def create_product(session: Session, product_data):
    product = Product(**product_data.dict())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_product(session: Session, product_id: int):
    return session.get(Product, product_id)

def get_all_products(session: Session):
    return session.exec(select(Product)).all()

def update_product(session: Session, product_id: int, product_data):
    product = session.get(Product, product_id)
    if not product:
        return None
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def delete_product(session: Session, product_id: int):
    product = session.get(Product, product_id)
    if not product:
        return None
    session.delete(product)
    session.commit()
    return product
