import uuid
import datetime

from src.common.database import Database
from src.models.post import Post


class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        if _id is None:
            self._id = uuid.uuid4().hex
        else:
            self._id = _id

    # ask user to write a new post
    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)

        post.save_to_mongo()  # save the post to mongoDB

    def get_post(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        # we return an OBJECT with relevant data
        return cls(**blog_data) # return the object element
        '''
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   _id=blog_data['_id'])
        '''

    # Find all blogs, serach by author_id
    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                                 query={'author_id': author_id})
        #return list of the blog objects
        return [cls(**blog) for blog in blogs]