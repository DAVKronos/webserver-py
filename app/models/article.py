from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from .user import User, UserPublic

class ArticleBase(SQLModel):
    created_at: datetime
    updated_at: datetime
    title: str
    title_en: str
    news: str
    news_en: str
    agreed: bool
    agreed_by: int
    articlephoto_updated_at: datetime
    articlephoto_url_normal: str
    articlephoto_url_carrousel: str


class ArticlePublic(ArticleBase):
    id: int
    user: UserPublic | None = None

class ArticlePublicWithCommentCount(ArticlePublic):
    comment_count: int
    
class Article(ArticleBase, table=True):
    __tablename__: str = "newsitems"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="articles", sa_relationship_kwargs={"lazy": "selectin"})

 
