from five import grok
from plone.directives import dexterity, form

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

class IProject(form.Schema, IImageScaleTraversable):
    """
    A specific project content type
    """
    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload main project image. A scaled version will be "
                      u"used in search results and project listings"),
        required=True,
    )
    text = RichText(
        title=_(u"Main Text"),
        description=_(u"Enter project description inluding project details"),
        required=True
    )
    form.fieldset(
        'details',
        label=_(u"Project Details"),
        fields=['contractor', 'architect', 'planning_period',
                'construction_period', 'construction_costs',
                'floor_space_title', 'floor_space',
                'floor_index_title', 'floor_space_index',
                'capacity_title', 'capacity', 'services']
    )
    contractor = schema.TextLine(
        title=_(u"Building Contractor"),
        required=False,
    )
    architect = schema.TextLine(
        title=_(u"Architect"),
        required=False,
    )
    planning_period = schema.TextLine(
        title=_(u"Planning Period"),
        required=False,
    )
    construction_period = schema.TextLine(
        title=_(u"Construction Period"),
        required=False
    )
    construction_costs = schema.TextLine(
        title=_(u"Construction Costs"),
        required=False,
    )
    floor_space_title = schema.TextLine(
        title=_(u"Floor Space Title"),
        required=False,
    )
    floor_space = schema.TextLine(
        title=_(u"Floor Space"),
        required=False,
    )
    floor_index_title = schema.TextLine(
        title=_(u"Floor Index Title"),
        required=False
    )
    floor_space_index = schema.TextLine(
        title=_(u"Floor Space Index"),
        required=False,
    )
    capacity_title = schema.TextLine(
        title=_(u"Capacity title"),
        required=False,
    )
    capacity = schema.TextLine(
        title=_(u"Cubic Capacity"),
        required=False,
    )
    services = schema.Text(
        title=_(u"ISP Services"),
        description=_(u"Enter ISP services one sentence per line. These will "
                      u"displayed as a bulleted list"),
        required=False,
    )


class Project(dexterity.Container):
    grok.implements(IProject)


class View(grok.View):
    grok.context(IProject)
    grok.require('zope2.View')
    grok.name('view')
