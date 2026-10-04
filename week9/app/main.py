from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query 
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select

from app.database import engine, SessionDep
from app.models import (
    Hero,
    HeroCreate,
    HeroPublic,
    HeroUpdate,
    Team,
    TeamCreate,
    TeamPublic,
    Mission,
    MissionCreate,
    MissionPublic,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hero API is running"}


@app.post("/heroes", response_model=HeroPublic, status_code=201)
def create_hero(hero: HeroCreate, session: SessionDep):
    if hero.team_id is not None:
        team = session.get(Team, hero.team_id)

        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

    db_hero = Hero.model_validate(hero)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)

    return db_hero


@app.get("/heroes", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None,
):
    statement = select(Hero)

    if min_age is not None:
        statement = statement.where(Hero.age >= min_age)

    if team_id is not None:
        statement = statement.where(Hero.team_id == team_id)

    if name is not None:
        statement = statement.where(Hero.name.ilike(f"%{name}%"))

    statement = statement.order_by(Hero.id).offset(offset).limit(limit)

    heroes = session.exec(statement).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    db_hero = session.get(Hero, hero_id)

    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)

    if "team_id" in hero_data and hero_data["team_id"] is not None:
        team = session.get(Team, hero_data["team_id"])

        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

    db_hero.sqlmodel_update(hero_data)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)

    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()

    return {"ok": True}

@app.post("/teams", response_model=TeamPublic, status_code=201)
def create_team(team_in: TeamCreate, session: SessionDep):
    team = Team.model_validate(team_in)
    session.add(team)

    try:
        session.commit()
        session.refresh(team)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Team already exists")

    return team

@app.get("/teams", response_model=list[TeamPublic])
def read_teams(session: SessionDep):
    teams = session.exec(select(Team).order_by(Team.id)).all()
    return teams

@app.get("/teams/{team_id}/heroes", response_model=list[HeroPublic])
def read_team_heroes(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return team.heroes

@app.post("/missions", response_model=MissionPublic, status_code=201)
def create_mission(mission_in: MissionCreate, session: SessionDep):
    mission = Mission.model_validate(mission_in)

    session.add(mission)
    session.commit()
    session.refresh(mission)

    return mission

@app.post(
    "/heroes/{hero_id}/missions/{mission_id}",
    status_code=204
)
def assign_mission(
    hero_id: int,
    mission_id: int,
    session: SessionDep
):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    mission = session.get(Mission, mission_id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission not in hero.missions:
        hero.missions.append(mission)
        session.add(hero)
        session.commit()

@app.get(
    "/heroes/{hero_id}/missions",
    response_model=list[MissionPublic]
)
def read_hero_missions(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    return hero.missions