from sqlmodel import Field, Relationship, SQLModel, and_
from datetime import datetime
from .user import User, UserPublic
from .comment import Comment
from sqlalchemy.orm import foreign

class ArticleBase(SQLModel):
    created_at: datetime
    updated_at: datetime
    title: str
    title_en: str
    news: str
    news_en: str
    agreed: bool
    agreed_by: int | None = None
    articlephoto_updated_at: datetime | None = None
    articlephoto_url_normal: str | None = None
    articlephoto_url_carrousel: str | None = None

class Article(ArticleBase, table=True):
    __tablename__: str = "newsitems"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="articles", sa_relationship_kwargs={"lazy": "selectin"})
    comments: list[Comment] = Relationship(sa_relationship_kwargs = {
        "primaryjoin": lambda: and_(Article.id==foreign(Comment.commentable_id), Comment.commentable_type=="Newsitem"),
        "lazy": "selectin" })

class ArticlePublic(ArticleBase):
    id: int
    user: UserPublic | None = None

class ArticlePublicWithCommentCount(ArticlePublic):
    comment_count: int

class ArticleCreate(SQLModel):
    title: str
    title_en: str
    news: str
    news_en: str

class ArticleUpdate(SQLModel):
    title: str | None = None
    title_en: str | None = None
    news: str | None = None
    news_en: str | None = None
