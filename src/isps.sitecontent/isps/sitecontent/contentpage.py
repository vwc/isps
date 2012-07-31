from five import grok
from plone.directives import dexterity, form
from plone.indexer import indexer

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

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
    return ' '.join([obj.Title(), obj.Description(), obj.text.output])
grok.global_adapter(searchableTextIndexer, name="SearchableText")


class ContentPage(dexterity.Item):
    grok.implements(IContentPage)


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')
