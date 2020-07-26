from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class PublishedArticlesManager(models.Manager):
    def get_query_set(self):
        return super(PublishedArticlesManager, self).get_query_set().filter(is_published=True)


class Article(models.Model):
    """Represents a wiki article"""

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    text = models.TextField(help_text="Formatted using ReST")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, verbose_name="Publish?")
    created_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    published = PublishedArticlesManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('wiki_article_detail', args=[], kwargs={'slug': self.slug})


class Edit(models.Model):
    """Stores an edit session"""

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    edited_on = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=100)

    class Meta:
        ordering = ['-edited_on']

    def __unicode__(self):
        return "%s - %s - %s" % (self.summary, self.editor, self.edited_on)

    def get_absolute_url(self):
        return reverse('wiki_edit_detail', self.id)