from five import grok
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.formwidget.autocomplete import AutocompleteFieldWidget
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from isps.sitecontent.contentpage import IContentPage
from isps.sitecontent.project import IProject

from isps.sitecontent import MessageFactory as _


# Interface class; used to define content-type schema.

class IBanner(form.Schema, IImageScaleTraversable):
    """
    Animated banner content
    """
    image = NamedBlobImage(
        title=_(u"Banner Image"),
        description=_(u"Upload banner image ideally already resized to the "
                      u"correct dimensions"),
        required=True,
    )
    form.widget(project=AutocompleteFieldWidget)
    project = RelationChoice(
        title=_(u"Project"),
        description=_(u"Select related project for the banner link"),
        source=ObjPathSourceBinder(object_provides=IProject.__identifier__),
        required=False,
    )
    information = RelationChoice(
        title=_(u"Related content"),
        description=_(u"Select related content. When a link to related "
                      u"content is available any selection for related "
                      u"projects will be ignored"),
        source=ObjPathSourceBinder(
            object_provides=IContentPage.__identifier__),
        required=False,
    )


class Banner(dexterity.Item):
    grok.implements(IBanner)


class View(grok.View):
    grok.context(IBanner)
    grok.require('zope2.View')
    grok.name('view')
