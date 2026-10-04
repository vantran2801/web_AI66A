from sqlmodel import Session, SQLModel, select

from app.database import engine
from app.models import Hero, Mission, Team


def seed():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        existing_team = session.exec(select(Team)).first()

        if existing_team:
            print("Database already contains teams. Skipping seed.")
            return

        avengers = Team(
            name="Avengers",
            headquarters="New York"
        )

        xmen = Team(
            name="X-Men",
            headquarters="Westchester"
        )

        mission1 = Mission(
            title="Save New York"
        )

        mission2 = Mission(
            title="Protect the World"
        )

        heroes = [
            Hero(
                name="Tony",
                age=45,
                secret_name="Iron Man",
                team=avengers,
                missions=[mission1]
            ),
            Hero(
                name="Natasha",
                age=35,
                secret_name="Black Widow",
                team=avengers,
                missions=[mission1, mission2]
            ),
            Hero(
                name="Logan",
                age=150,
                secret_name="Wolverine",
                team=xmen,
                missions=[mission2]
            ),
            Hero(
                name="Scott",
                age=35,
                secret_name="Cyclops",
                team=xmen,
                missions=[mission2]
            ),
            Hero(
                name="Peter",
                age=16,
                secret_name="Spider-Man",
                missions=[mission1]
            ),
        ]

        session.add(avengers)
        session.add(xmen)
        session.add_all(heroes)

        session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed()