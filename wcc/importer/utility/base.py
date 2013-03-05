from five import grok
from wcc.importer.interfaces import IImporter
from zope.container.interfaces import INameChooser
import time
import transaction

class BaseImporter(grok.GlobalUtility):
    grok.implements(IImporter)
    grok.baseclass()

    def run_import(self, container, data):
        for entry in data:
            self._factory(container, entry)

    def _factory(self):
        raise NotImplementedError

    def _create_obj_for_title(self, container, portal_type, title):
        oid = container.invokeFactory(type_name=portal_type, id=time.time())
        transaction.savepoint(optimistic=True)
        obj = container._getOb(oid)
        # set id
        oid = INameChooser(container).chooseName(title, obj)
        obj.setId(oid)
        obj.setTitle(title)
        return oid


