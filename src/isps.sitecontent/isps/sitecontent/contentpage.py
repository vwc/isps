from five import grok
from plone.directives import dexterity, form
from plone.indexer import indexer

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage
from plone.app.textfield import RichText

from Products.CMFPlone.utils import safe_unicode

from isps.sitecontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IContentPage(form.Schema, IImageScaleTraversable):
    """
    A basic content page with preview image
    """
    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload optional preview image used in listings and "
                      u"search results"),
        required=False,
    )
    text = RichText(
        title=_(u"Main Text"),
        required=True,
    )


@indexer(IContentPage)
def searchableTextIndexer(obj):
    return ' '.join([safe_unicode(obj.Title()),
                     safe_unicode(obj.Description()),
                     obj.text.output])
grok.global_adapter(searchableTextIndexer, name="SearchableText")


class ContentPage(dexterity.Item):
    grok.implements(IContentPage)


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')
