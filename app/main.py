from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login
@app.post("/login")
def login():
    return {"token": auth.create_token()}

@app.post("/guest", dependencies=[Depends(auth.verify_token)])
def add_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    new_guest = models.Guest(**guest.dict())
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest

@app.get("/guest", dependencies=[Depends(auth.verify_token)])
def get_guests(db: Session = Depends(get_db)):
    return db.query(models.Guest).all()

def send_sms(name: str, amount: int):
    import time
    time.sleep(3)
    print(f"[Background Task]: SMS Sent to '{name}' - Shukriya ₹{amount}")

@app.patch("/shagun/{guest_id}", dependencies=[Depends(auth.verify_token)])
def update_shagun(
    guest_id: int,
    data: schemas.GuestUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()

    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    guest.shagun_amount = data.amount
    guest.status = "Arrived"
    db.commit()

    # Background task
    background_tasks.add_task(send_sms, guest.name, data.amount)

    return {"message": "Lifafa recorded!"}

@app.delete("/guest/{guest_id}", dependencies=[Depends(auth.verify_token)])
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(models.Guest).filter(models.Guest.id == guest_id).first()

    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    db.delete(guest)
    db.commit()

    return {"message": "Guest removed"}
