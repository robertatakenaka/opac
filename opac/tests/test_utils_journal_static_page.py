# coding: utf-8

import os
from .base import BaseTestCase

from . import utils

from webapp.utils.journal_static_page import JournalStaticPageFile
from webapp.utils.utils import get_new_page


FIXTURE_PATH = 'opac/tests/pages'
FIXTURE2_PATH = 'opac/tests/revistas'
acron_list = sorted(os.listdir(FIXTURE2_PATH))
file_names = {'en': ['iaboutj.htm',
                     'iedboard.htm',
                     'iinstruc.htm'],
              'pt_BR': ['paboutj.htm',
                        'pedboard.htm',
                        'pinstruc.htm'],
              'es': ['eaboutj.htm',
                     'eedboard.htm',
                     'einstruc.htm'],
              }
IMG_LOCATION_ALT = 'opac/tests/img_revistas'


class GetNewPagesTestCase(BaseTestCase):

    def test_all_pages(self):
        not_found = []
        images = []
        for acron in acron_list:
            for lang, files in file_names.items():
                journal_pages_path = os.path.join(FIXTURE2_PATH, acron)
                content, images_in_file = get_new_page(
                    journal_pages_path, files)
                images.extend(images_in_file)
                for img_in_file in images_in_file:
                    basename = os.path.basename(img_in_file)
                    img_in_fs = os.path.join(journal_pages_path, basename)

                    if not os.path.isfile(img_in_fs):
                        dirname = os.path.dirname(img_in_file)
                        if '/img/revistas' in dirname:
                            p = dirname.find('/img/revistas')
                            subdirs = dirname[p+len('/img/revistas'):]
                            img_in_fs = os.path.join(
                                IMG_LOCATION_ALT + subdirs, basename)
                            if not os.path.isfile(img_in_fs):
                                not_found.append(
                                    (acron, img_in_file, img_in_fs))
        open('images_in_file.txt', 'w').write(
            '\n'.join(sorted(list(set(images)))))
        open('images.log', 'w').write(
            '\n'.join([str(item) for item in not_found]))
        self.assertEqual(open('journal_pages.log').read(), '')
        self.assertEqual(open('images.log').read(), '')


class JournalStaticPageTestCase(BaseTestCase):

    def html_file(self, name):
        return os.path.join(FIXTURE_PATH, name.replace('_', '/')+'.htm')

    def test_insert_bold_to_p_subtitulo_aa_eedboard(self):
        jspf = JournalStaticPageFile(self.html_file('aa_eedboard'))

        self.assertEqual(jspf.body_content.count('class="subtitulo"'), 4)
        self.assertTrue(
            '<p class="subtitulo"><a name="001">Editor-Jefe</a></p>'
            in jspf.body_content
        )
        self.assertTrue(
            '<p class="subtitulo"><a name="0011"></a>Editor-Jefe Sustituto</p>'
            in jspf.body_content)
        self.assertTrue(
            '<p class="subtitulo">Comisión editorial</p>' in
            jspf.body_content)
        jspf._insert_bold_to_p_subtitulo()
        self.assertEqual(jspf.body_content.count('class="subtitulo"'), 0)
        self.assertTrue(
            '<p><b>Comisión editorial</b></p>' in jspf.body_content)
        self.assertTrue(
            '<p><b><a name="001">Editor-Jefe</a></b></p>' in jspf.body_content
        )
        self.assertTrue(
            '<p><a name="0011"></a><b>Editor-Jefe Sustituto</b></p>'
            in jspf.body_content)

    def test_remove_anchors_abb_pinstruc(self):
        jspf = JournalStaticPageFile(self.html_file('abb_pinstruc'))
        self.assertTrue('<a name="end"></a>' in jspf.body_content)
        jspf._remove_anchors()
        self.assertTrue('<a name="end"></a>' not in jspf.body_content)

    def test_remove_anchors_aa_eedboard(self):
        jspf = JournalStaticPageFile(self.html_file('aa_eedboard'))

        self.assertEqual(jspf.body_content.count('class="subtitulo"'), 4)
        self.assertTrue(
            '<p class="subtitulo"><a name="001">Editor-Jefe</a></p>'
            in jspf.body_content
        )
        self.assertTrue(
            '<p class="subtitulo"><a name="0011"></a>Editor-Jefe Sustituto</p>'
            in jspf.body_content)

        self.assertTrue('<a name="0011"' in jspf.body_content)
        jspf._remove_anchors()
        self.assertTrue(
            '<p class="subtitulo">Editor-Jefe Sustituto</p>'
            in jspf.body_content)

    def test_middle_text_ea_pinstruc(self):
        jspf = JournalStaticPageFile(self.html_file('ea_pinstruc'))
        text = '<p>6. As Referências bibliográficas deverão ser citadas'
        self.assertTrue(text in jspf.middle_text)

    def test_read_iso_8859_1_eagri_pedboard(self):
        jspf = JournalStaticPageFile(self.html_file('eagri_pedboard'))
        self.assertTrue('Agrícola' in jspf.body_content)
        self.assertTrue('Associação' in jspf.body_content)

    def test_insert_middle_begin_abb_pinstruc(self):
        jspf = JournalStaticPageFile(self.html_file('abb_pinstruc'))
        self.assertTrue('Editable' in jspf.body_content)
        self.assertFalse('"middle_begin"' in jspf.body_content)
        jspf.insert_middle_begin()
        self.assertTrue('"middle_begin"' in jspf.body_content)

    def test_insert_middle_begin_aa_eedboard(self):
        jspf = JournalStaticPageFile(self.html_file('aa_eedboard'))
        self.assertTrue('href="#0' in jspf.body_content)
        self.assertFalse('"middle_begin"' in jspf.body_content)
        jspf.insert_middle_begin()
        self.assertTrue('"middle_begin"' in jspf.body_content)

    def test_insert_middle_begin_ea_iinstruc(self):
        jspf = JournalStaticPageFile(self.html_file('ea_iinstruc'))
        self.assertTrue('script=sci_serial' in jspf.body_content)
        self.assertFalse('"middle_begin"' in jspf.body_content)
        jspf.insert_middle_begin()
        self.assertTrue('"middle_begin"' in jspf.body_content)

    def test_insert_middle_begin_eins_eedboard(self):
        jspf = JournalStaticPageFile(self.html_file('eins_eedboard'))
        self.assertTrue('/scielo.php?lng=' in jspf.body_content)
        self.assertFalse('"middle_begin"' in jspf.body_content)
        jspf.insert_middle_begin()
        self.assertTrue('"middle_begin"' in jspf.body_content)

    def test_middle_end_abb_pinstruc(self):
        jspf = JournalStaticPageFile(self.html_file('abb_pinstruc'))
        self.assertTrue('javascript:history.back()' in jspf.body_content)
        self.assertFalse('"middle_end"' in jspf.body_content)
        jspf.insert_middle_end()
        self.assertTrue('"middle_end"' in jspf.body_content)

    def test_insert_middle_end_aa_eedboard(self):
        jspf = JournalStaticPageFile(self.html_file('aa_eedboard'))
        self.assertTrue('script=sci_serial' in jspf.body_content)
        self.assertTrue('Home' in jspf.body_content)
        self.assertFalse('"middle_end"' in jspf.body_content)
        jspf.insert_middle_end()
        self.assertTrue('"middle_end"' in jspf.body_content)

    def test_insert_middle_end_bjmbr_iedboard(self):
        jspf = JournalStaticPageFile(self.html_file('bjmbr_iedboard'))
        self.assertTrue('script=sci_serial' in jspf.body_content)
        self.assertTrue('Home' in jspf.body_content)

        self.assertFalse('"middle_end"' in jspf.body_content)
        jspf.insert_middle_end()
        self.assertTrue('"middle_end"' in jspf.body_content)

    def test_insert_middle_end_bjgeo_pinstruct(self):
        jspf = JournalStaticPageFile(self.html_file('bjgeo_pinstruct'))
        self.assertTrue('script=sci_serial' in jspf.body_content)
        self.assertTrue('Voltar' in jspf.body_content)
        self.assertFalse('"middle_end"' in jspf.body_content)
        jspf.insert_middle_end()
        self.assertTrue('"middle_end"' in jspf.body_content)

    def test_insert_middle_end_bjgeo_einstruct(self):
        jspf = JournalStaticPageFile(self.html_file('bjgeo_einstruct'))
        self.assertTrue('script=sci_serial' in jspf.body_content)
        self.assertTrue('Volver' in jspf.body_content)
        self.assertFalse('"middle_end"' in jspf.body_content)
        jspf.insert_middle_end()
        self.assertTrue('"middle_end"' in jspf.body_content)

    def test_unavailable_msg_es_abb_einstruc(self):
        jspf = JournalStaticPageFile(self.html_file('abb_einstruc'))
        self.assertTrue(jspf.ES_UNAVAILABLE_MSG in jspf.unavailable_message)

    def test_unavailable_message_pt_abb_pinstruc(self):
        jspf = JournalStaticPageFile(self.html_file('abb_pinstruc'))
        self.assertTrue(jspf.PT_UNAVAILABLE_MSG in jspf.unavailable_message)
