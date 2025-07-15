# scripts/seed_roles.py
from sqlmodel import Session, select, SQLModel
from app.db.models import Role, RoleName
from app.db.session import engine

def main() -> None:
    #print("Starting database setup...")
    #print("Dropping all tables...")
    #drop_all_tables() # wipe db
    print("Creating all tables...")
    SQLModel.metadata.create_all(engine) # create tables
    with Session(engine) as session:
        print("Populating roles...")
        populate_roles(session)
        # Verify roles were created
        roles = session.exec(select(Role)).all()
        print(f"Created roles: {[role.name for role in roles]}")

def populate_roles(session: Session) -> None:
    """
    Seed the roles table with predefined roles.
    This function is called at application startup.
    """
    print(f"Available roles to create: {[rn.value for rn in RoleName]}")
    for rn in RoleName:
        role_exists = session.exec(select(Role).where(Role.name == rn)).first()
        if not role_exists:
            print(f"Creating role: {rn.value}")
            session.add(Role(name=rn))
    session.commit()

def drop_all_tables() -> None:
    """
    Drops ALL tables!
    """
    SQLModel.metadata.drop_all(engine)

if __name__ == "__main__":
    main()
