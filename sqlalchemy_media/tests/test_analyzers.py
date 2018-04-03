import unittest
import io
from os.path import dirname, abspath, join

from sqlalchemy_media.processors import ImageAnalyzer, MagicAnalyzer, WandAnalyzer
from sqlalchemy_media.descriptors import AttachableDescriptor


class AnalyzerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.this_dir = abspath(dirname(__file__))
        cls.stuff_path = join(cls.this_dir, 'stuff')
        cls.cat_jpeg = join(cls.stuff_path, 'cat.jpg')
        cls.cat_png = join(cls.stuff_path, 'cat.png')

    def test_magic(self):
        # guess content types from extension

        analyzer = MagicAnalyzer()

        with AttachableDescriptor(io.BytesIO(b'Simple text')) as d:
            ctx = {}
            analyzer.process(d, ctx)
            self.assertEqual(ctx['content_type'], 'text/plain')

        with AttachableDescriptor(self.cat_jpeg) as d:
            ctx = {}
            analyzer.process(d, ctx)
            self.assertEqual(ctx['content_type'], 'image/jpeg')

        with AttachableDescriptor(self.cat_png) as d:
            ctx = {}
            analyzer.process(d, ctx)
            self.assertEqual(ctx['content_type'], 'image/png')

    def test_wand(self):
        analyzer = WandAnalyzer()
        with AttachableDescriptor(self.cat_jpeg) as d:
            ctx = {}
            analyzer.process(d, ctx)
            self.assertDictEqual(ctx, {
                'width': 640,
                'height': 480,
                'content_type': 'image/jpeg'
            })

    def test_wand_generic(self):
        from sqlalchemy_media.imaginglibs import use_wand, reset_choice
        use_wand()
        try:
            analyzer = ImageAnalyzer()
            with AttachableDescriptor(self.cat_jpeg) as d:
                ctx = {}
                analyzer.process(d, ctx)
                self.assertDictEqual(ctx, {
                    'width': 640,
                    'height': 480,
                    'content_type': 'image/jpeg'
                })
        finally:
            reset_choice()

    def test_pil(self):
        from sqlalchemy_media.imaginglibs import use_pil, reset_choice
        use_pil()
        try:
            analyzer = ImageAnalyzer()
            with AttachableDescriptor(self.cat_jpeg) as d:
                ctx = {}
                analyzer.process(d, ctx)
                self.assertDictEqual(ctx, {
                    'width': 640,
                    'height': 480,
                    'content_type': 'image/jpeg'
                })
        finally:
            reset_choice()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
