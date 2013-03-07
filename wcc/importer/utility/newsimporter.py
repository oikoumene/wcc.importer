from five import grok
import dateutil.parser
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
import logging
logger = logging.getLogger("wcc.importer")
from base64 import b64decode
from wcc.importer.utility.base import BaseImporter

class NewsImporter(BaseImporter):
    grok.name('wcc.importer.newsimporter')

    def _factory(self, container, entry):
        logger.info("Creating News Item : %s" % entry['title'])

        oid = self._create_obj_for_title(container, 'News Item', entry['title'])
        obj = container._getOb(oid)

        # set description
        obj.setDescription(entry['description'])

        # set effectiveDate
        d,m,y = entry['effectiveDate'].split('.')
        edate = dateutil.parser.parse('%s-%s-%s' % (y,m,d))
        obj.getField('effectiveDate').set(obj, edate)

        # set bodytext
        obj.getField('text').set(obj, entry['bodytext'])
        
        # set image
        if entry.has_key('image'):
            try:
                obj.getField('image').set(obj, 
                        b64decode(entry['image']))
            except:
                logger.info(
                    "Unable to import image for : %s" % obj.absolute_url()
                )

        if entry.has_key('imageCaption'):
            obj.getField('imageCaption').set(obj, entry['imageCaption'])

        # remember original url
        anno = IAnnotations(obj)
        anno.setdefault('wcc.metadata', PersistentDict())
        anno['wcc.metadata']['original_url'] = entry['orig_url']
        anno['wcc.metadata']['lang_urls'] = entry['lang_urls']
        obj.reindexObject()

        logger.info("Created %s" % obj.absolute_url())
