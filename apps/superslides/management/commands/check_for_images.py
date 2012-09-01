"""
check_for_slides.py

Provides a django management command
that reads the default upload directory
for a given slideshow.

  Default path:
      /public/media/slideshows/<slug>/slides/
"""

import sys
from datetime import datetime
from optparse import make_option


from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import smart_str
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType


class Command(NoArgsCommand):
    """Command object for importing a Wordpress blog
    into Zinnia via Wordpress XML-RPC APIs."""
    help = 'Import a Wordpress blog into Zinnia via an XML-RPC interface.'

    option_list = NoArgsCommand.option_list + (
        make_option('--url', dest='url', default='',
                    help='The url, including xmlrpc to login to your blog'),
        make_option('--username', dest='username', default='',
                    help='Username to log into Blog with'),
        )

    SITE = Site.objects.get_current()

    def __init__(self):
        """Init the Command and add custom styles"""
        super(Command, self).__init__()
        self.style.TITLE = self.style.SQL_FIELD
        self.style.STEP = self.style.SQL_COLTYPE
        self.style.ITEM = self.style.HTTP_INFO

    def write_out(self, message, verbosity_level=1):
        """Convenient method for outputing"""
        if self.verbosity and self.verbosity >= verbosity_level:
            sys.stdout.write(smart_str(message))
            sys.stdout.flush()

    def handle_noargs(self, **options):
        try:
            from wordpress_xmlrpc import Client, WordPressPost
            from wordpress_xmlrpc.methods.taxonomies import GetTerms
            from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
            from wordpress_xmlrpc.methods.users import GetUserInfo, GetAuthors
        except ImportError:
            raise CommandError('You need to install the ' \
                               'python-wordpress-xmlrpc module.')

        self.verbosity = int(options.get('verbosity', 1))
        self.url= options.get('url')
        self.username= options.get('username')

        self.write_out(self.style.TITLE(
            'Starting migration from Wordpress to Zinnia \n'))

        if not self.url:
            self.url= raw_input('Wordpress url: ')
            if not self.url:
                raise CommandError('Invalid Wordpress url')

        if not self.username:
            self.username = raw_input('Wordpress username: ')
            if not self.username:
                raise CommandError('Invalid Wordpress username')

        self.password = getpass('Wordpress password: ')

        try:
            blog = Client(self.url, self.username, self.password)
        except:
            raise CommandError('Incorrect Wordpress URL, username or password')

        self.write_out(self.style.STEP('> Connecting to server: %s \n' % self.url))
        self.write_out(self.style.STEP('> Looking up authors...\n'))
        authors = blog.call(GetAuthors())
        self.write_out(self.style.STEP('> Found %s authors\n' % len(authors)))

        increment = 20
        offset = 340 
        while True:
            self.write_out(self.style.STEP('> Looking up posts...\n'))
            posts = blog.call(GetPosts({'number':increment, 'offset':offset}))
            self.write_out(self.style.STEP('> Found %s posts\n' % len(posts)))
            if len(posts) == 0:
                break # no more posts returned
            for post in posts:
                author_name= self.lookup_author(post.user, authors)
                author=self.get_or_create_author(author_name)
                terms=self.get_terms_from_post(post)

                try:
                    entry = Entry.objects.get(creation_date=post.date,
                                              slug=slugify(post.title))
                    output = self.write_out(self.style.NOTICE('> Skipped %s (already imported)\n' % entry))
                except Entry.DoesNotExist:
                    entry = Entry.objects.create(
                        id=post.id,
                        title=post.title,
                        content=post.content.replace('\n', '<br />'),
                        status=2, # found in zinnia.managers
                        slug=slugify(post.title),
                        creation_date=post.date,
                        last_update=post.date_modified,
                        comment_enabled=False,
                        pingback_enabled=False)
                    entry.tags=' '.join([t.name for t in terms['tags']])
                    entry.save()
                    entry.sites.add(self.SITE)
                    [entry.categories.add(c) for c in terms['categories']]
                    entry.authors.add(author)
                    self.write_out(self.style.ITEM('> Migrated %s + no comments\n'
                        % (entry.title)))
                except:
                    self.write_out(self.style.NOTICE(
                        'Failed to import: %s\n' % post.title))
                offset = offset + increment
            self.write_out(self.style.TITLE('Completed importing %s posts\n' % increment))
        return True

    def lookup_author(self, id, authors):
        for author in authors:
            if author.id == id:
                return author.display_name

    def get_terms_from_post(self, post=None):
        cats=[]
        tags=[]
        for t in post.terms:
            if t.taxonomy == 'category':
                cats.append(self.get_or_create_category(t))
            elif t.taxonomy == 'post_tag':
                tags.append(self.get_or_create_tag(t))
        return {'categories':cats,'tags':tags}


    def get_or_create_author(self, author_name=''):
        try:
            user = User.objects.get(username=slugify(author_name))
        except:
            first = author_name.split(' ')[0]
            last = ' '.join(author_name.split(' ')[1:])
            user= User.objects.create(
                         username=slugify(author_name),
                         first_name=first,
                         last_name=last,
                         is_staff=True
                     )
            user.save()
        return user

    def get_or_create_tag(self, tag=None):
        tag_name = tag.name + ','
        try:
            t = Tag.objects.get(name=tag_name)
        except:
            t = Tag.objects.create(name=tag_name)
            t.save()
        return t

    def get_or_create_category(self, category=None):
        try:
            c = Category.objects.get(Q(title=category.name)|Q(slug=slugify(category.name)))
        except:
            c = Category.objects.create(title=category.name,
                slug=slugify(category.name))
            c.save() 
        return c
