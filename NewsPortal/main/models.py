from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
    """
    Модель, содержащая объекты всех авторов.
    Имеет следующие поля:
    - cвязь «один к одному» с встроенной моделью пользователей User;
    - рейтинг пользователя.
    """
    rating_author = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def update_rating(self):
        """
        Обновляет рейтинг пользователя.
        Он состоит из следующего:
        - суммарный рейтинг каждой статьи автора умножается на 3;
        - суммарный рейтинг всех комментариев автора;
        - суммарный рейтинг всех комментариев к статьям автора.
        """
        
        # Суммарный рейтинг каждой статьи автора умножается на 3
        sum_rating_post = sum([x['rating_content'] for x in self.post_set.all().values()]) * 3 
        
        # Cуммарный рейтинг всех комментариев автора
        sum_rating_comment_author = sum([x['rating_comment'] for x in Comment.objects.filter(user = self.author_id).values()])
         
        # Посты автора, что найти все комменты к его постам
        post_author = self.post_set.all()     #Post.objects.filter(author = self)
        # Cуммарный рейтинг всех комментариев к статьям автора
        sum_rating_comment_post_author = sum([x['rating_comment'] for x in  Comment.objects.filter(post__in = post_author).values()])

        self.rating_author = sum_rating_post + sum_rating_comment_author + sum_rating_comment_post_author
        self.save()


class Category(models.Model):
    """
    Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.). 
    Имеет единственное поле: название категории. Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
    """
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    """
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
    Соответственно, модель должна включать следующие поля:
    - связь «один ко многим» с моделью Author;
    - поле с выбором — «статья» или «новость»;
    - автоматически добавляемая дата и время создания;
    - связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    - заголовок статьи/новости;
    - текст статьи/новости;
    - рейтинг статьи/новости.
    """
    news = 'NEWS'
    article = 'article'
    CONTENT = [(news, 'новость'), (article, 'статья')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_content = models.CharField(max_length = 7, choices = CONTENT, default = news)
    date_create_post = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating_content = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_content += 1
        self.save()
    
    def dislike(self):
        self.rating_content -= 1
        self.save()
        
    def preview(self):
        """
        Возвращает начало статьи (предварительный просмотр) 
        длиной 124 символа и добавляет многоточие в конце.
        """
        preview = self.text[0:124] + '...'
        
        return preview


class PostCategory(models.Model):
    """
    Промежуточная модель для связи «многие ко многим»:
    - связь «один ко многим» с моделью Post;
    - связь «один ко многим» с моделью Category.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля:
    связь «один ко многим» с моделью Post;
    связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    текст комментария;
    дата и время создания комментария;
    рейтинг комментария.
    """    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date_create_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    
    def like(self):
        self.rating_comment += 1
        self.save()
        
    def dislike(self):
        self.rating_comment -= 1
        self.save()