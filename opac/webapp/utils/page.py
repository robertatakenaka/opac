# coding=utf-8

import os
import logging
import requests
import tempfile

from webapp.utils import create_image, create_file  # noqa


from bs4 import BeautifulSoup
from slugify import slugify


LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)
fh = logging.FileHandler('page.log', mode='w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def new_author_url_page(old_url):
    # http://www.scielo.br/cgi-bin/wxis.exe/iah/
    # ?IsisScript=iah/iah.xis&base=article%5Edlibrary&format=iso.pft&
    # lang=p&nextAction=lnk&
    # indexSearch=AU&exprSearch=MEIERHOFFER,+LILIAN+KOZSLOWSKI
    # ->
    # //search.scielo.org/?q=au:MEIERHOFFER,+LILIAN+KOZSLOWSKI')
    if 'indexSearch=AU' in old_url and 'exprSearch=' in old_url:
        name = old_url[old_url.rfind('exprSearch=')+len('exprSearch='):]
        if '&' in name:
            name = name[:name.find('&')]
        return '//search.scielo.org/?q=au:{}'.format(
            name.replace(' ', '+')
        )
    return old_url


def slugify_filename(file_location, used_names):
    file_basename = os.path.basename(file_location)
    file_name, file_ext = os.path.splitext(file_basename)
    if file_location is not None:
        alt_name = slugify(file_name) + file_ext
        if used_names.get(alt_name) in [None, file_basename]:
            new_file_name = alt_name
        else:
            new_file_name = file_basename
        used_names[new_file_name] = file_basename
        return new_file_name
    return file_basename


def downloaded_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(tempfile.mkdtemp(), os.path.basename(url))
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path


def confirm_file_location(file_location, file_path):
    try:
        # Verifica se a imagem existe
        if file_location is None:
            return False
        open(file_location)
        return True
    except IOError as e:
        logging.error(
            u'%s (corresponding to %s)' % (e, file_path))
        return False


def delete_file(file_path):
    try:
        # Verifica se a imagem existe
        os.remove(file_path)
    except IOError as e:
        logging.error(
            u'%s (corresponding to %s)' % (e, file_path))
    else:
        logging.error(
            u'%s (corresponding to %s)' % (e, file_path))


class Page(object):

    def __init__(self, content, original_website, revistas_path,
                 img_revistas_path,
                 static_files_path=None, page_name=None, lang=None):
        self.original_website = original_website
        self.revistas_path = revistas_path
        self.img_revistas_path = img_revistas_path
        self.static_files_path = static_files_path
        self.lang = lang
        self.page_name = page_name
        self.content = content
        self.used_names = {}
        self.INVALID_TEXT_IN_URL = None
        self.prefixes = [self.page_name, self.lang]

    @property
    def content(self):
        return str(self.tree)

    @content.setter
    def content(self, value):
        self.tree = BeautifulSoup(value, 'lxml')

    @property
    def original_website(self):
        return self._original_website

    @original_website.setter
    def original_website(self, value):
        website = value
        if '//' in website:
            website = website[website.find('//')+2:]
        if website.endswith('/'):
            website = website[:-1]
        self._original_website = website

    def migrate_urls(self):
        replacements = []
        for elem_name, attr_name in [('a', 'href'), ('img', 'src')]:
            for elem in self.find_original_website_reference(
                    elem_name, attr_name):
                old_url = str(elem[attr_name])
                new_url = self.get_new_url(old_url)
                if new_url != old_url:
                    replacements.append((old_url, new_url))
                    old_display_text = elem.string
                    elem[attr_name] = new_url
                    new_display_text = self.link_display_text(
                        new_url, old_display_text, old_url)
                    if new_display_text != old_display_text:
                        elem.string = new_display_text

        replacements = list(sorted(set(replacements)))
        for old, new in replacements:
            q = self.content.count(old)
            if q > 0:
                logging.info(
                    'CONFERIR: ainda existe: {} ({})'.format(old, q))

    def _fix_invalid_url(self, url):
        if self.INVALID_TEXT_IN_URL and self.INVALID_TEXT_IN_URL in url:
            return url.replace(self.INVALID_TEXT_IN_URL, '')
        return url

    def replace_by_relative_url(self, url):
        # www.scielo.br/revistas/icse/levels.pdf -> /revistas/icse/levels.pdf
        #
        # www.scielo.br/img/revistas/icse/levels.pdf ->
        # /img/revistas/icse/levels.pdf
        #
        # http://www.scielo.br/scielo.php?script=sci_serial&pid=0102-4450&lng=en&nrm=iso
        # -> /scielo.php?script=sci_serial&pid=0102-4450&lng=en&nrm=iso
        #
        # http://www.scielo.br -> /
        if self.original_website in url:
            p = url.find(self.original_website) + len(self.original_website)
            url = url[p:].strip()
            for relative in ['/scielo.php', '/img/revistas', '/revistas']:
                if relative in url:
                    return url[url.find(relative):]
            if '/fbpe' in url:
                return url[url.find('/fbpe')+len('/fbpe'):]
            if url == '':
                return '/'
        return url

    def get_new_url(self, url):
        url = self._fix_invalid_url(url)
        if url.strip().count(' ') > 0:
            return url

        if 'cgi-bin' in url and 'indexSearch=AU' in url:
            return new_author_url_page(url)

        if self.original_website in url:
            return self.replace_by_relative_url(url)
        return url

    def link_display_text(self, link, display_text, original_url):
        if display_text is not None:
            text = display_text.strip().replace('&nbsp;', '')
            if text == original_url:
                return '{}{}'.format(self.original_website,
                                     text.replace(original_url, link))
            elif original_url.endswith(text):
                return '{}{}'.format(self.original_website, link)
        return display_text

    def find_original_website_reference(self, elem_name, attribute_name):
        mentions = []
        for item in self.tree.find_all(elem_name):
            value = item.get(attribute_name, '')
            if self.original_website in value:
                mentions.append(item)
        return mentions

    @property
    def images(self):
        return [img
                for img in self.tree.find_all('img')
                if img.get('src')]

    @property
    def files(self):
        return [item
                for item in self.tree.find_all('a')
                if item.get('href')]

    def guess_file_location(self, file_path):
        if '/img/revistas/' in file_path:
            return os.path.join(
                self.img_revistas_path,
                file_path[file_path.find('/img/revistas/') +
                          len('/img/revistas/'):])
        if '/revistas/' in file_path:
            return os.path.join(
                self.revistas_path,
                file_path[file_path.find('/revistas/') +
                          len('/revistas/'):])
        if self.static_files_path:
            if self.original_website in file_path:
                location = file_path[file_path.find(self.original_website) +
                                     len(self.original_website):]
                return os.path.join(self.static_files_path, location[1:])
            elif file_path.startswith('/'):
                location = file_path[1:]
                return os.path.join(self.static_files_path, location)

    def get_prefixed_slug_name(self, img_location):
        new_img_name = slugify_filename(img_location, self.used_names)

        _prefixes = self.prefixes + [new_img_name]
        parts = [part for part in _prefixes if part is not None]
        return '_'.join(parts)

    def is_asset_url(self, referenced):
        name, ext = os.path.splitext(referenced)
        if ext.lower() in ['.pdf', '.html', '.htm', '.jpg', '.png', '.gif']:
            return 'https://{}{}'.format(self.original_website, referenced)

    def get_file_info(self, referenced):
        file_location = self.guess_file_location(referenced)
        valid_path = confirm_file_location(file_location, referenced)
        url = None
        if not valid_path:
            url = self.is_asset_url(referenced)
            if url:
                file_location = downloaded_file(url)
                valid_path = confirm_file_location(file_location, referenced)
        if valid_path:
            file_dest_name = self.get_prefixed_slug_name(file_location)
            return (file_location, file_dest_name, url is not None)
        logging.info('CONFERIR: {} não encontrado'.format(referenced))

    def create_images(self, images=None, migrate_url=True):
        if migrate_url and self.original_website in self.content:
            self.migrate_urls()
        for image in images or self.images:
            src = image.get('src')
            if ':' not in src:
                image_info = self.get_file_info(src)
                if image_info:
                    img_src, img_dest, is_temp = image_info
                    image['src'] = self._register_image(img_src, img_dest)

    def create_files(self, files=None, migrate_url=True):
        if migrate_url and self.original_website in self.content:
            self.migrate_urls()
        for _file in files or self.files:
            href = _file.get('href')
            if ':' not in href:
                _file_info = self.get_file_info(href)
                if _file_info:
                    _file_href, _file_dest, is_temp = _file_info
                    _file['href'] = self._register_file(_file_href, _file_dest)

    def _register_image(self, img_src, img_dest):
        img = create_image(img_src, img_dest, check_if_exists=False)
        delete_file(img_src)
        return img.get_absolute_url

    def _register_file(self, source, destination):
        _file = create_file(source, destination, check_if_exists=False)
        delete_file(source)
        return _file.get_absolute_url


class JournalPage(Page):

    anchors = {
        'about': 'aboutj',
        'editors': 'edboard',
        'instructions': 'instruc',
    }

    def __init__(self, content, original_website, revistas_path,
                 img_revistas_path, acron,
                 static_files_path=None, page_name=None, lang=None):
        super().__init__(content, original_website, revistas_path,
                         img_revistas_path, static_files_path, page_name, lang)
        self.acron = acron
        self.prefixes = [acron]
        """
        ERRADO: http://www.scielo.br/revistas/icse/www1.folha.uol.com.br
        CORRETO: http://www1.folha.uol.com.br
        """
        self.INVALID_TEXT_IN_URL = '{}/revistas/{}/www'.format(
            self.original_website, acron)

    @property
    def original_journal_home_page(self):
        if self.acron:
            return '{}/{}'.format(self.original_website, self.acron)
        return ''

    @property
    def new_journal_home_page(self):
        if self.acron:
            return '/journal/{}/'.format(self.acron)
        return ''

    def new_about_journal_page(self, anchor):
        if self.acron:
            if anchor in self.anchors.keys():
                return self.new_journal_home_page+'about/#'+anchor
            return self.new_journal_home_page+'about'
        return ''

    def get_new_url(self, url):
        # www.scielo.br/icse -> /journal/icse/
        if url.lower().endswith(self.original_journal_home_page):
            return self.new_journal_home_page

        # www.scielo.br/revistas/icse/iaboutj.htm -> /journal/icse/about/#about
        if url.endswith('.htm') and '/{}/'.format(self.acron) in url:
            for new, old in self.anchors.items():
                if old in url:
                    return self.new_about_journal_page(new)

        return super().get_new_url(url)