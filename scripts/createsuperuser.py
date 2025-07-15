import argparse
import getpass
from sqlmodel import Session, select, SQLModel
from app.db.session import engine  # Import engine instead of get_session
from app.db.models import User, Role
from app.core import security
from scripts.seed_roles import populate_roles

def main():
    """
    Create a superuser (admin) for the application.
    Command: python -m scripts.createsuperuser --username <username> --password <password>
    If flags are omitted, prompts interactively.
    """
    parser = argparse.ArgumentParser(description="Create a superuser (admin)")
    parser.add_argument("--username", required=False)
    parser.add_argument("--password", required=False)
    parser.add_argument("--dropall", required=False)
    args = parser.parse_args()

    username = args.username or input("Username: ")
    password = args.password or getpass.getpass("Password: ")
    dropall = args.dropall or input("Drop all users (y/N): ")

    if dropall == "y":
        print("Dropping all tables...")
        SQLModel.metadata.drop_all(engine)
        print("Creating all tables...")
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            populate_roles(session)

    with Session(engine) as session:

        admin_role = session.exec(select(Role).where(Role.name == "admin")).first()
        if not admin_role:
            print("Admin role does not exist. Please seed roles first.")
            return

        if session.exec(select(User).where(User.username == username)).first():
            print("User already exists.")
            return

        user = User(
            username=username,
            password_hash=security.hash_password(password),
            role_id=admin_role.id,
        )
        session.add(user)
        session.commit()
        print(f"Superuser '{username}' created.")

if __name__ == "__main__":
    main()