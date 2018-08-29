# coding: utf-8

import os
from .base import BaseTestCase

from . import utils

from webapp.utils.journal_static_page import JournalStaticPageFile, get_new_journal_page, get_journal_page_img_paths


REVISTAS_PATH = 'opac/tests/fixtures/pages/revistas'
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
IMG_REVISTAS_PATH = 'opac/tests/fixtures/pages/img_revistas'


class UtilsJournalPagesTestCase(BaseTestCase):

    def test_rbep_get_new_journal_page(self):
        expected = [
                    '/img/revistas/rbep/CNPq logo.gif',
                    '/img/revistas/rbep/Logotipo Financiador 1 - FACED.jpg',
                    '/img/revistas/rbep/Logotipo Financiador 2 - PROPESQ.jpg',
                    '/img/revistas/rbep/Logotipo Financiador 3 -PAEP.jpg',
                    '/img/revistas/rbep/Logotipo Instituição Mantenedora.jpg',
                    ]
        journal_pages_path = os.path.join(REVISTAS_PATH, 'rbep')
        files = ['paboutj.htm', 'pedboard.htm', 'pinstruc.htm']
        content, images_in_file = get_new_journal_page(
                                            journal_pages_path, files)
        self.assertEqual(expected, images_in_file)

    def test_rbep_get_journal_page_img_paths(self):
        PATH = '/img/revistas/'
        images_in_file = [
                    PATH+'rbep/CNPq logo.gif',
                    PATH+'rbep/Logotipo Financiador 1 - FACED.jpg',
                    PATH+'rbep/Logotipo Financiador 2 - PROPESQ.jpg',
                    PATH+'rbep/Logotipo Financiador 3 -PAEP.jpg',
                    PATH+'rbep/Logotipo Instituição Mantenedora.jpg',
                    ]

        expected = []
        expected += [(PATH+'rbep/CNPq logo.gif',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/CNPq logo.gif'),
                      'rbep_cnpq-logo.gif'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Financiador 1 - FACED.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Financiador 1 - FACED.jpg'),
                      'rbep_logotipo-financiador-1-faced.jpg'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Financiador 2 - PROPESQ.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Financiador 2 - PROPESQ.jpg'),
                      'rbep_logotipo-financiador-2-propesq.jpg'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Financiador 3 -PAEP.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Financiador 3 -PAEP.jpg'),
                      'rbep_logotipo-financiador-3-paep.jpg'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Instituição Mantenedora.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Instituição Mantenedora.jpg'),
                      'rbep_logotipo-instituicao-mantenedora.jpg'
                      )
                     ]
        expected = sorted(expected)
        journal_img_paths = get_journal_page_img_paths(
                                'rbep',
                                images_in_file,
                                REVISTAS_PATH,
                                IMG_REVISTAS_PATH
                                )
        for expected_item, img_path in zip(expected, journal_img_paths):
            self.assertEqual(expected_item, img_path)

    def test_aa_get_new_journal_page(self):
        expected = [
                    '/img/revistas/rbep/CNPq logo.gif',
                    '/img/revistas/rbep/Logotipo Financiador 1 - FACED.jpg',
                    '/img/revistas/rbep/Logotipo Financiador 2 - PROPESQ.jpg',
                    '/img/revistas/rbep/Logotipo Financiador 3 -PAEP.jpg',
                    '/img/revistas/rbep/Logotipo Instituição Mantenedora.jpg',
                    ]
        journal_pages_path = os.path.join(REVISTAS_PATH, 'rbep')
        files = ['paboutj.htm', 'pedboard.htm', 'pinstruc.htm']
        content, images_in_file = get_new_journal_page(
                                            journal_pages_path, files)
        self.assertEqual(expected, images_in_file)

    def test_aa_get_journal_page_img_paths(self):
        PATH = '/img/revistas/'
        images_in_file = [
                    PATH+'rbep/CNPq logo.gif',
                    PATH+'rbep/Logotipo Financiador 1 - FACED.jpg',
                    PATH+'rbep/Logotipo Financiador 2 - PROPESQ.jpg',
                    PATH+'rbep/Logotipo Financiador 3 -PAEP.jpg',
                    PATH+'rbep/Logotipo Instituição Mantenedora.jpg',
                    ]

        expected = []
        expected += [(PATH+'rbep/CNPq logo.gif',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/CNPq logo.gif'),
                      'rbep_cnpq-logo.gif'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Financiador 1 - FACED.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Financiador 1 - FACED.jpg'),
                      'rbep_logotipo-financiador-1-faced.jpg'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Financiador 2 - PROPESQ.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Financiador 2 - PROPESQ.jpg'),
                      'rbep_logotipo-financiador-2-propesq.jpg'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Financiador 3 -PAEP.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Financiador 3 -PAEP.jpg'),
                      'rbep_logotipo-financiador-3-paep.jpg'
                      )
                     ]
        expected += [(PATH+'rbep/Logotipo Instituição Mantenedora.jpg',
                      os.path.join(
                            IMG_REVISTAS_PATH,
                            'rbep/Logotipo Instituição Mantenedora.jpg'),
                      'rbep_logotipo-instituicao-mantenedora.jpg'
                      )
                     ]
        expected = sorted(expected)
        journal_img_paths = get_journal_page_img_paths(
                                'rbep',
                                images_in_file,
                                REVISTAS_PATH,
                                IMG_REVISTAS_PATH
                                )
        for expected_item, img_path in zip(expected, journal_img_paths):
            self.assertEqual(expected_item, img_path)


class JournalStaticPageTestCase(BaseTestCase):

    def html_file(self, name):
        return os.path.join(REVISTAS_PATH, name.replace('_', '/')+'.htm')

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
