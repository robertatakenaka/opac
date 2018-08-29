# coding=utf-8

import os
import logging

from bs4 import BeautifulSoup, Comment, element
from slugify import slugify


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('journal_pages.log', mode='w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def get_new_journal_page(journal_pages_path, files):
    """
    Extract the header and the footer of the page
    Insert the anchor based on filename
    """
    content = []
    img_paths = []
    unavailable_message = None
    for file in files:
        file_path = os.path.join(journal_pages_path, file)
        page = JournalStaticPageFile(file_path)
        if page.unavailable_message:
            content.append(page.anchor)
            unavailable_message = page.unavailable_message
        else:
            content.append(page.body)
            img_paths.extend(page.img_paths)
    if unavailable_message is not None:
        content.append(unavailable_message)
    return '\n'.join(content), sorted(list(set(img_paths)))


def find_journal_page_img_file(img_in_file, acron, revistas_path,
                               img_revistas_path):
    img_basename = os.path.basename(img_in_file)
    revistas_acron_path = os.path.join(revistas_path, acron)
    location = os.path.join(revistas_acron_path, img_basename)
    if not os.path.isfile(location):
        if '/img/revistas/' in img_in_file:
            location = os.path.join(
                img_revistas_path,
                img_in_file[img_in_file.find('/img/revistas/') +
                            len('/img/revistas/'):])
        elif '/revistas/' in img_in_file:
            location = os.path.join(
                revistas_path,
                img_in_file[img_in_file.find('/revistas/')+len('/revistas/'):])
    try:
        # Verifica se a imagem existe
        open(location)
    except IOError as e:
        logging.error(
            u'%s (corresponding to %s)' % (e, img_in_file))
    else:
        return location


def img_new_name(img_location, used_names):
    img_basename = os.path.basename(img_location)
    img_name, img_ext = os.path.splitext(img_basename)
    if img_location is not None:
        alt_name = slugify(img_name) + img_ext
        if alt_name not in used_names:
            new_img_name = alt_name
        else:
            new_img_name = img_basename
        used_names.append(new_img_name)
        return new_img_name


def get_journal_page_img_paths(acron, images_in_file, revistas_path,
                            img_revistas_path):
    used_names = []
    images = []
    for img_in_file in images_in_file:
        img_location = find_journal_page_img_file(img_in_file,
                                                      acron,
                                                      revistas_path,
                                                      img_revistas_path)
        if img_location is not None:
            new_img_name = img_new_name(img_location, used_names)
            img_dest_name = '%s_%s' % (acron, new_img_name)
            images.append((img_in_file, img_location, img_dest_name))
    return images


class JournalStaticPage(object):

    # about, editors, instructions, contact
    # 'iaboutj.htm', 'iedboard.htm', 'iinstruc.htm'
    anchors = {
        'about': 'about',
        'editors': 'edboard',
        'instructions': 'instruc',
    }

    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    @property
    def header(self):
        _header = None
        if '<table' in self.content:
            _header = self.content[self.content.find('<table'):]
            _header = _header[:_header.find('</table>')+len('</table>')]
            _header = _header.strip()
            if _header.startswith('<table') and _header.endswith('</table>'):
                pass
            else:
                print(self.filename, 'header', 'unexpected format')
                _header = None
        return _header

    @property
    def footer(self):
        _footer = None
        if 'script=sci_serial' in self.content:
            p = self.content.rfind('script=sci_serial')
            _footer = self.content[:p]
            p = _footer.rfind('<p ')
            _footer = self.content[p:]
            _footer = _footer[:_footer.find('</body>')]
            _footer = _footer.strip()
            if _footer.startswith('<p') and _footer.endswith('</p>'):
                pass
            else:
                print(self.filename, 'footer', 'unexpected format')
                _footer = None
        return _footer

    @property
    def anchor(self):
        _anchor = None
        for anchor_name, name in self.anchors.items():
            if name in self.filename:
                _anchor = anchor_name
                break
        if _anchor is not None:
            return '<a name="{}">'.format(_anchor)
        return ''

    @property
    def body(self):
        if all([self.header, self.footer]):
            new = self.content.replace(self.header, self.anchor)
            new = new.replace(self.footer, '<hr noshade="" size="1"/>')
            return new
        return self.content


class JournalStaticPageFile(object):

    # about, editors, instructions, contact
    # 'iaboutj.htm', 'iedboard.htm', 'iinstruc.htm'
    anchors = {
        'about': 'about',
        'editors': 'edboard',
        'instructions': 'instruc',
    }
    versions = {'p': 'português', 'e': 'español', 'i': 'English'}
    PT_UNAVAILABLE_MSG = 'Informação não disponível em português. ' + \
                         'Consultar outra versão. '
    ES_UNAVAILABLE_MSG = 'Información no disponible en español. ' + \
                         'Consultar otra versión. '

    def __init__(self, filename):
        self.filename = filename
        self.name = os.path.basename(filename)
        self.version = self.versions[self.name[0]]
        self.get_tree()

    def get_tree(self):
        for parser in ['lxml', 'html.parser']:
            if parser is not None:
                self.tree = BeautifulSoup(self.file_content, parser)
            if self.middle_end_insertion_position is None:
                self._info('Not found: end. FAILED {}'.format(parser))
            elif self.middle_begin_insertion_position is None:
                self._info('Not found: begin. FAILED {}'.format(parser))
            else:
                break

    @property
    def _body_tree(self):
        if self.tree is not None:
            if self.tree.body is not None:
                return self.tree.body
        return self.tree

    @property
    def tree_content(self):
        if self.tree is None:
            return self.file_content
        return str(self.tree)

    @property
    def body_content(self):
        if self._body_tree is not None:
            return str(self._body_tree)

    def _info(self, msg):
        logger.debug('%s %s' % (self.filename, msg))

    @property
    def file_content(self):
        _content = None
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                _content = f.read()
        except UnicodeError:
            with open(self.filename, 'r', encoding='iso-8859-1') as f:
                _content = f.read()
                self._info('iso-8859-1')
        except Exception as e:
            self._info(u'%s' % e)
            logging.error(u'%s' % e)
        return _content or ''

    def _remove_anchors(self):
        items = self._body_tree.find_all('a')
        for item in items:
            name = item.get('name')
            if name is not None:
                if item.string:
                    item.insert_after(item.string)
                item.extract()

    def _insert_bold_to_p_subtitulo(self):
        p_items = self._body_tree.find_all('p')
        for p in p_items:
            style = p.get('class')
            if style is not None:
                if 'subtitulo' in list(style):
                    if not p.find_all('b'):
                        del p['class']
                        for item in p.children:
                            new_tag = self.tree.new_tag("b")
                            wrap(item, new_tag)

    @property
    def p_middle_begin(self):
        items = [p
                 for p in self._body_tree.find_all('p')
                 if p.get('id', '') == 'middle_begin']
        if len(items) == 1:
            return items[0]

    @property
    def middle_begin_insertion_position(self):
        table = self._body_tree.find('table')
        if table is not None:
            header = str(table)
            if has_header(header):
                return table

    def insert_middle_begin(self):
        if self.p_middle_begin is None:
            table = self.middle_begin_insertion_position
            if table is not None:
                new_tag = self.tree.new_tag("p")
                new_tag['id'] = 'middle_begin'
                table.insert_after(new_tag)
                return new_tag
        return self.p_middle_begin

    @property
    def p_middle_end(self):
        items = [p
                 for p in self._body_tree.find_all('p')
                 if p.get('id', '') == 'middle_end']
        if len(items) == 1:
            return items[0]

    @property
    def middle_end_insertion_position(self):
        p = None
        href_items = []
        a_items = self._body_tree.find_all('a')
        for a in a_items:
            href = a.get('href')
            if href is not None:
                href = str(href).strip()
                href_items.append((a, href, a.text))
                if has_footer(href, a):
                    p = a.parent
                    break
        if p is None:
            for hr in self._body_tree.find_all('hr'):
                p = hr
            if p is not None:
                self._info('footer hr')
        if p is not None:
            return p

    def insert_middle_end(self):
        if self.p_middle_end is None:
            p = self.middle_end_insertion_position
            if p is not None:
                new_tag = self.tree.new_tag("p")
                new_tag['id'] = 'middle_end'
                p.insert_before(new_tag)
                return new_tag
        return self.p_middle_end

    def _get_middle_children_eval_child(self, child, p_begin, p_end, task):
        if task == 'find_p_begin':
            if child == p_begin:
                task = 'find_p_end'
            return task, None
        if task == 'find_p_end' and child == p_end:
            return 'stop', None
        if isinstance(child, Comment):
            return task, None
        return task, child

    def _get_middle_children(self, p_begin, p_end):
        task = 'find_p_begin'
        items = []
        for child in self._body_tree.children:
            task, item = self._get_middle_children_eval_child(
                child, p_begin, p_end, task)
            if item is not None:
                items.append(item)
            elif task == 'stop':
                break
        return items

    @property
    def anchor_name(self):
        for anchor_name, name in self.anchors.items():
            if name in self.filename:
                return anchor_name

    @property
    def anchor(self):
        _anchor = self.anchor_name
        if _anchor is not None:
            return '<a name="{}"> </a>'.format(_anchor)
        return ''

    def _check_unavailable_message(self, content):
        if self.version == 'português' and 'não disponível' in content:
            return self.PT_UNAVAILABLE_MSG
        elif self.version == 'español' and 'no disponible' in content:
            return self.ES_UNAVAILABLE_MSG

    def _get_unavailable_message(self):
        self._unavailable_message = None
        text = self._check_unavailable_message(self.body_content)
        if text:
            p_items = self.sorted_by_relevance
            msg = self._check_unavailable_message(p_items[0][1])
            if msg is not None:
                self._info(len(p_items[0][1]))
                self._info(p_items[0][1][:200])
                if len(p_items[0][1]) < 200:
                    self._unavailable_message = '<p>{}</p>'.format(msg)
                    self._info(self._unavailable_message)
                else:
                    self._info('IGNORED')

    @property
    def sorted_by_relevance(self):
        return sorted([(len(p), p) for p in self.middle_items], reverse=True)

    @property
    def middle_children(self):
        if not hasattr(self, '_middle_children'):
            self._remove_anchors()
            self._insert_bold_to_p_subtitulo()
            begin = self.insert_middle_begin()
            end = self.insert_middle_end()
            self._middle_children = self._get_middle_children(begin, end)
        return self._middle_children

    @property
    def middle_items(self):
        if not hasattr(self, '_middle_items'):
            self._middle_items = [child_tostring(item)
                                  for item in self.middle_children]
        return self._middle_items

    @property
    def middle_text(self):
        if not hasattr(self, '_middle_text'):
            self._middle_text = ''.join([str(item)
                                         for item in self.middle_children])
        return self._middle_text

    @property
    def unavailable_message(self):
        self._get_unavailable_message()
        return self._unavailable_message

    @property
    def img_paths(self):
        _img_paths = []
        for child in self.middle_children:
            if isinstance(child, element.Tag):
                for img in child.find_all('img'):
                    src = img.get('src')
                    if src is not None and '://' not in src:
                        _img_paths.append(src)
        return _img_paths

    @property
    def alternative_middle_text(self):
        middle = self.file_content
        if '</table>' in middle:
            middle = middle[middle.find('</table>')+len('</table>'):]
        if 'Home' in middle:
            middle = middle[:middle.rfind('Home')]
            middle = middle[:middle.rfind('<p')]
        elif 'Volver' in middle:
            middle = middle[:middle.rfind('Volver')]
            middle = middle[:middle.rfind('<p')]
        elif 'Voltar' in middle:
            middle = middle[:middle.rfind('Voltar')]
            middle = middle[:middle.rfind('<p')]
        if '</body>' in middle:
            middle = middle[:middle.rfind('</body>')]
        return middle

    @property
    def body(self):
        if self.p_middle_end is None:
            middle = self.alternative_middle_text
        else:
            middle = self.middle_text

        return '<!-- inicio {} -->'.format(self.filename) + \
               self.anchor + middle + '<hr noshade="" size="1"/>' + \
               '<!-- fim {} -->'.format(self.filename)


def has_header(content):
    return 'Editable' in content and '<!--' in content and '-->' in content or\
           'href="#0' in content or \
           'script=sci_serial' in content or \
           '/scielo.php?lng=' in content


def has_footer(href, a=None):
    if a is not None:
        return '#' == href and a.text.strip() == 'Home' or \
               'script=sci_serial' in href and a.text.strip() == 'Home' or \
               'script=sci_serial' in href and a.text.strip() == 'Voltar' or \
               'script=sci_serial' in href and a.text.strip() == 'Volver' or \
               'javascript:history.back()' == href
    return 'script=sci_serial' in href and 'Home' in href or \
           'script=sci_serial' in href and 'Voltar' in href or \
           'script=sci_serial' in href and 'Volver' in href or \
           'javascript:history.back()' in href


def remove_exceding_space_chars(content):
    parts = content.split()
    return ' '.join([p for p in parts if len(p) > 0])


def child_tostring(child):
    if isinstance(child, element.Tag):
        return child.text
    elif isinstance(child, element.NavigableString):
        return child


def wrap(child, new_tag):
    if isinstance(child, element.Tag):
        if child.string is not None:
            child.wrap(new_tag)
    elif isinstance(child, element.NavigableString):
        return child.wrap(new_tag)

