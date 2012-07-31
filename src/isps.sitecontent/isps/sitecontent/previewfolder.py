from five import grok
from Acquisition import aq_inner
from plone.directives import dexterity, form

from Products.CMFCore.utils import getToolByName
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.contentlisting.interfaces import IContentListing
from isps.sitecontent.project import IProject
from isps.sitecontent.contentpage import IContentPage

from isps.sitecontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IPreviewFolder(form.Schema, IImageScaleTraversable):
    """
    Folder with optional image previews
    """
    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload preview image that will be displayed inside "
                       "the dropdown menu"),
        required=False,
    )


class PreviewFolder(dexterity.Container):
    grok.implements(IPreviewFolder)


class View(grok.View):
    grok.context(IPreviewFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_projects = len(self.contained_projects()) > 0

    def contained_items(self):
        if self.has_projects:
            return self.contained_projects()
        else:
            return self.contained_pages()

    def contained_projects(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IProject.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

    def contained_pages(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IContentPage.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist
