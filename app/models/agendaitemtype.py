from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class AgendaitemTypeBase(SQLModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    name_en: str
    is_match: bool | None

class AgendaitemType(AgendaitemTypeBase, table=True):
    __tablename__: str = "agendaitemtypes"
    id: int | None = Field(default=None, primary_key=True)
    agendaitems: list["Agendaitem"] = Relationship(back_populates="agendaitemtype")

class AgendaitemTypeResponse(AgendaitemTypeBase):
    name: str
    name_en: str
