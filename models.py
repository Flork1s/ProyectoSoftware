from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --------------------------
# Link table: Build <-> Component (Many-to-Many)
# --------------------------
class BuildComponentLink(SQLModel, table=True):
    build_id: Optional[int] = Field(
        default=None, foreign_key="build.id", primary_key=True
    )
    component_id: Optional[int] = Field(
        default=None, foreign_key="component.id", primary_key=True
    )


# --------------------------
# Link table: Component <-> Category (Many-to-Many)
# --------------------------
class ComponentCategoryLink(SQLModel, table=True):
    component_id: Optional[int] = Field(
        default=None, foreign_key="component.id", primary_key=True
    )
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )


# --------------------------
# User (1) -> (N) Build
# --------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    image_url: Optional[str] = None

    builds: List["Build"] = Relationship(back_populates="user")

class UserCreate(SQLModel):
    name: str
    email: str
    image_url: Optional[str] = None


# --------------------------
# Build: belongs to User, has many Components (via link), has one Configuration (1:1)
# --------------------------
class Build(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="builds")
    # many-to-many to Component
    components: List["Component"] = Relationship(
        back_populates="builds", link_model=BuildComponentLink
    )
    # one-to-one: configuration
    configuration: Optional["Configuration"] = Relationship(
        back_populates="build", sa_relationship_kwargs={"uselist": False}
    )

    @property
    def total_price(self) -> float:
        return sum(c.price for c in self.components)

class BuildCreate(SQLModel):
    name: str
    user_id: int

# --------------------------
# Component: many-to-many with Build, many-to-many with Category
# --------------------------
class Component(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    kind: str
    brand: str
    price: float

    builds: List[Build] = Relationship(
        back_populates="components", link_model=BuildComponentLink
    )
    categories: List["Category"] = Relationship(
        back_populates="components", link_model=ComponentCategoryLink
    )
class ComponentCreate(SQLModel):
    name: str
    kind: str
    brand: str
    price: float
    build_id: int | None = None


# --------------------------
# Category: many-to-many with Component
# --------------------------
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    components: List[Component] = Relationship(
        back_populates="categories", link_model=ComponentCategoryLink
    )


# --------------------------
# Configuration: one-to-one with Build
# --------------------------
class Configuration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    build_id: Optional[int] = Field(default=None, foreign_key="build.id", unique=True)

    os: Optional[str] = None
    bios_version: Optional[str] = None

    build: Optional[Build] = Relationship(
        back_populates="configuration", sa_relationship_kwargs={"uselist": False}
    )