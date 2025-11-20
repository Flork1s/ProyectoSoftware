# crud.py
from sqlmodel import Session, select
from models import User, Build, Component, Category, Configuration, BuildComponentLink, ComponentCategoryLink

# ---------------- USERS ----------------
def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session):
    return session.exec(select(User)).all()

def get_user(session: Session, user_id: int):
    return session.get(User, user_id)

def update_user(session: Session, user_id: int, data: dict):
    user = session.get(User, user_id)
    if not user:
        return None
    for k, v in data.items():
        setattr(user, k, v)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return user

# ---------------- BUILDS ----------------
def create_build(session: Session, build: Build) -> Build:
    session.add(build)
    session.commit()
    session.refresh(build)
    return build

def get_builds(session: Session):
    return session.exec(select(Build)).all()

def get_build(session: Session, build_id: int):
    return session.get(Build, build_id)

def update_build(session: Session, build_id: int, data: dict):
    build = session.get(Build, build_id)
    if not build:
        return None
    for k, v in data.items():
        setattr(build, k, v)
    session.add(build)
    session.commit()
    session.refresh(build)
    return build

def delete_build(session: Session, build_id: int):
    build = session.get(Build, build_id)
    if not build:
        return None
    session.delete(build)
    session.commit()
    return build

# ---------------- COMPONENTS ----------------
def create_component(session: Session, comp: Component) -> Component:
    session.add(comp)
    session.commit()
    session.refresh(comp)
    return comp

def get_components(session: Session):
    return session.exec(select(Component)).all()

def get_component(session: Session, component_id: int):
    return session.get(Component, component_id)

def update_component(session: Session, component_id: int, data: dict):
    comp = session.get(Component, component_id)
    if not comp:
        return None
    for k, v in data.items():
        setattr(comp, k, v)
    session.add(comp)
    session.commit()
    session.refresh(comp)
    return comp

def delete_component(session: Session, component_id: int):
    comp = session.get(Component, component_id)
    if not comp:
        return None
    session.delete(comp)
    session.commit()
    return comp

# ---------------- CATEGORIES ----------------
def create_category(session: Session, cat: Category) -> Category:
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat

def get_categories(session: Session):
    return session.exec(select(Category)).all()

def get_category(session: Session, category_id: int):
    return session.get(Category, category_id)

def update_category(session: Session, category_id: int, data: dict):
    cat = session.get(Category, category_id)
    if not cat:
        return None
    for k, v in data.items():
        setattr(cat, k, v)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat

def delete_category(session: Session, category_id: int):
    cat = session.get(Category, category_id)
    if not cat:
        return None
    session.delete(cat)
    session.commit()
    return cat

# ---------------- CONFIGURATION (1:1) ----------------
def create_configuration(session: Session, config: Configuration) -> Configuration:
    session.add(config)
    session.commit()
    session.refresh(config)
    return config

def get_configuration(session: Session, config_id: int):
    return session.get(Configuration, config_id)

def update_configuration(session: Session, config_id: int, data: dict):
    cfg = session.get(Configuration, config_id)
    if not cfg:
        return None
    for k, v in data.items():
        setattr(cfg, k, v)
    session.add(cfg)
    session.commit()
    session.refresh(cfg)
    return cfg

def delete_configuration(session: Session, config_id: int):
    cfg = session.get(Configuration, config_id)
    if not cfg:
        return None
    session.delete(cfg)
    session.commit()
    return cfg

# ---------------- LINKS helpers (Many-to-Many) ----------------
def add_component_to_build(session: Session, build_id: int, component_id: int):
    # ensure both exist
    build = session.get(Build, build_id)
    comp = session.get(Component, component_id)
    if not build or not comp:
        return None
    link = BuildComponentLink(build_id=build_id, component_id=component_id)
    session.add(link)
    session.commit()
    return {"message": "linked"}

def remove_component_from_build(session: Session, build_id: int, component_id: int):
    stmt = select(BuildComponentLink).where(
        (BuildComponentLink.build_id == build_id) & (BuildComponentLink.component_id == component_id)
    )
    res = session.exec(stmt).first()
    if not res:
        return None
    session.delete(res)
    session.commit()
    return {"message": "unlinked"}

def add_category_to_component(session: Session, component_id: int, category_id: int):
    comp = session.get(Component, component_id)
    cat = session.get(Category, category_id)
    if not comp or not cat:
        return None
    link = ComponentCategoryLink(component_id=component_id, category_id=category_id)
    session.add(link)
    session.commit()
    return {"message": "linked"}
