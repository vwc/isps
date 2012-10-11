import math
from five import grok
from Acquisition import aq_inner
from zope import schema
from zope.component import getMultiAdapter
from plone.directives import dexterity, form

from Products.CMFCore.utils import getToolByName
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.contentlisting.interfaces import IContentListing
from plone.app.blob.interfaces import IATBlobImage
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
                      u"the dropdown menu"),
        required=False,
    )
    hide_children = schema.Bool(
        title=_(u"Hide children?"),
        description=_(u"Please select if you would like to hide the children."
                      u"This setting disables the dropdown menu in the "
                      u"main navigation for this folder."),
        required=False,
    )
    full_listing = schema.Bool(
        title=_(u"Enable full content listing"),
        description=_(u"Select full content listing if you want the folder to "
                      u"show both preview folder and content page subitems"),
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
        self.has_subfolders = len(self.subfolders()) > 0

    def construct_full_listing(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type=['isps.sitecontent.previewfolder',
                                       'isps.sitecontent.contentpage'],
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='getObjPositionInParent',
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

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
                          sort_on='getObjPositionInParent',
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

    def contained_pages(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IContentPage.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='getObjPositionInParent',
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist

    def subfolders(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IPreviewFolder.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='getObjPositionInParent',
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist


class GalleryView(grok.View):
    grok.context(IPreviewFolder)
    grok.require('zope2.View')
    grok.name('gallery-view')

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
            info['original_width'] = original['width']
            info['original_height'] = original['height']
            data.append(info)
        return data

    def image_matrix(self):
        items = self.image_list()
        count = len(items)
        rowcount = count / 5.0
        rows = math.ceil(rowcount)
        matrix = []
        for i in range(int(rows)):
            row = []
            for j in range(5):
                index = 5 * i + j
                if index <= int(count - 1):
                    cell = {}
                    cell['item'] = items[index]
                    row.append(cell)
            matrix.append(row)
        return matrix

    def getImageTag(self, item, scalename):
        if IATBlobImage.providedBy(item):
            obj = item
        else:
            obj = item.getObject()
        scales = getMultiAdapter((obj, self.request), name='images')
        if scalename == 'thumb':
            scale = scales.scale('image', width=100, height=100)
        else:
            scale = scales.scale('image', width=500, height=500)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        return item


class RecentView(grok.View):
    grok.context(IPreviewFolder)
    grok.require('zope2.View')
    grok.name('recent-view')

    def update(self):
        self.has_items = len(self.collect_items()) > 0

    def collect_items(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IContentPage.__identifier__,
                          path=dict(query='/'.join(context.getPhysicalPath()),
                                    depth=1),
                          sort_on='release_date',
                          sort_order='reverse',
                          review_state='published')
        resultlist = IContentListing(results)
        return resultlist
