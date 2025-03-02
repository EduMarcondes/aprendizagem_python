from app import models
from app.database import engine
from app.schemas import Products
from fastapi import FastAPI,Depends, HTTPException, Response,status
from app.database import get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/product")
def get_products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products

@app.post("/product")
def create(product: Products, db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.delete("/delete/{id}")
def delete(id:int,db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    delete_product = db.query(models.Product).filter(models.Product.id == id)

    if delete_product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    else:
        delete_product.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/update/{id}")
def update(id:int,product:Products,db: Session = Depends(get_db)):
    update_product = db.query(models.Product).filter(models.Product.id == id)
    
    if update_product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    else:
        update_product.update(product.dict(), synchronize_session=False)
        db.commit()
        return update_product.first()