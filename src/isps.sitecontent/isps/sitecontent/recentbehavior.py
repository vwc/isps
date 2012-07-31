from five import grok
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from Products.Five.utilities.marker import mark, erase

from isps.sitecontent.contentpage import IContentPage

from isps.sitecontent import MessageFactory as _


class IRecentMarker(Interface):
    """ Interface to mark content pages as recent """


class IRecentEventBehavior(form.Schema):
    """ Marker interface and fieldset for extending a content page with
        dates metadata
    """
    form.fieldset(
        'recentevent',
        label=_(u"Recent Event Behavior"),
        fields=['recent', 'release_date']
    )
    recent = schema.Bool(
        title=_(u"Mark as recent event"),
        description=_(u"Enable recent event behavior to list this item as "
                      u"current or recent event/project"),
        required=False,
    )
    release_date = schema.Datetime(
        title=_(u"Release Date"),
        description=_(u"Enter a date to provide chronological order for "
                      u"recent events and projects"),
        required="False",
    )

alsoProvides(IRecentEventBehavior, IFormFieldProvider)


@grok.subscribe(IContentPage, IObjectModifiedEvent)
def applyRecentMarker(obj, event):
    recent = obj.recent
    if recent == True:
        mark(obj, IRecentMarker)
    else:
        erase(obj, IRecentMarker)
    obj.reindexObject(idxs=['object_provides'])
