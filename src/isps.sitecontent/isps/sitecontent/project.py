import math
from Acquisition import aq_inner
from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.component import getMultiAdapter

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText
from Products.CMFCore.utils import getToolByName

from plone.app.blob.interfaces import IATBlobImage

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

    def update(self):
        self.has_images = len(self.contained_images()) > 0

    def contained_images(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IATBlobImage.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1))
        return results

    def image_list(self):
        context = aq_inner(self.context)
        images = self.contained_images()
        data = []
        for item in images:
            info = {}
            info['title'] = item.Title
            thumb = self.getImageTag(item, scalename='thumb')
            info['thumb_url'] = thumb['url']
            info['thumb_width'] = thumb['width']
            info['thumb_height'] = thumb['height']
            original = self.getImageTag(item, scalename='original')
            info['original_url'] = original['url']
            info['original_width'] = thumb['width']
            info['original_height'] = thumb['height']
            data.append(info)
        projectimg = {}
        projectimg['title'] = context.Title
        thumbnail = self.getImageTag(context, scalename='thumb')
        projectimg['thumb_url'] = thumbnail['url']
        projectimg['thumb_width'] = thumbnail['width']
        projectimg['thumb_height'] = thumbnail['height']
        original = self.getImageTag(context, scalename='original')
        projectimg['original_url'] = original['url']
        projectimg['original_width'] = original['width']
        projectimg['original_height'] = original['height']
        data.append(projectimg)
        return data

    def image_matrix(self):
        items = self.contained_images()
        count = len(items)
        rowcount = count / 4.0
        rows = math.ceil(rowcount)
        matrix = []
        for i in range(int(rows)):
            row = []
            for j in range(4):
                index = 4 * i + j
                if index <= int(count - 1):
                    cell = {}
                    cell['item'] = items[index]
                    row.append(cell)
            matrix.append(row)
        return matrix

    def getImageTag(self, item, scalename):
        obj = item.getObject()
        scales = getMultiAdapter((obj, self.request), name='images')
        if scalename == 'thumb':
            scale = scales.scale('image', width=100, height=100)
        else:
            scale = scales.scale('image', width=600, height=400)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        return item
