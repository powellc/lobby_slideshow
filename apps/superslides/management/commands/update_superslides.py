"""
updatesuperslides.py

Flow:

1. Read files in upload directory for superslides.
2. Get list of all slides from db
3. Compare file list to current slide list
  a. If slide found in db but not in directory: delete
  b. If slide found in dir but not in db: add
"""


import sys
import os

from django.utils.encoding import smart_str
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand
from superslides.models import Slide
from django.core.files import File

from PIL import Image
def is_image(filename):
    print filename
    try:
        im=Image.open(filename)
        return True
    except IOError:
        return False

class Command(NoArgsCommand):
    help = 'Updates slides in the upload directory'

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
        self.verbosity = int(options.get('verbosity', 1))
        self.media_path = getattr(settings, 'MEDIA_ROOT')
        self.path = os.path.join(self.media_path, getattr(settings, 'SUPERSLIDES_ROOT'))
        self.size=getattr(settings, 'SUPERSLIDES_SLIDE_SIZE')

        self.write_out(self.style.TITLE(
            'Checking superslide upload directory for changes...\n'))

        # Get list of jpeg files in the upload directory
        self.files = []
        try:
            for file in os.listdir(self.path):
                if is_image(os.path.join(self.path,file)):
                    # Also, sort out east_thumbnail cache files
                    if file.find(self.size) == -1:
                        self.files.append(file)
        except:
            raise CommandError('Problem reading directory, make sure SUPERSLIDES_ROOT variable set in settings.py')

        # Get a list of all the slides in the DB
        slides = Slide.objects.all()

        # First, check for slides in the dbs who's uploaded file has been deleted
        # Or, if we made a mistake and created slide without an image
        for slide in slides:
            try:
                with open(slide.image.path) as file: pass
            except IOError:
                slide.delete()
            except ValueError:
                slide.delete()

        # Next, compare the DB list with the directory list
        # Create any db objects if a new file exists
        for file in self.files:
            print file
            try:
                # First, check if the slide exists in the DB
                slide = Slide.objects.get(image=self.path+file)
                print '%s: Already in DB' % slide
            except:
                # If not, add it
                file_path = os.path.join(self.path, file)
                f = File(open(file_path, 'r'))
                slide = Slide.objects.create(name=file.split('.')[0])
                slide.image.save(file_path, f, True)
                slide.save()
                print '%s: Not in DB, added' % slide
