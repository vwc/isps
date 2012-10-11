from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IContentish

from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.viewlets.interfaces import IPortalFooter

from isps.sitecontent.recentbehavior import IRecentMarker


class RecentViewlet(grok.Viewlet):
    grok.name('isps.sitecontent.RecentViewlet')
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalFooter)

    def update(self):
        self.has_items = len(self.recent_items()) > 0

    def recent_items(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(object_provides=IRecentMarker.__identifier__,
                          review_state='published',
                          sort_on='release_date',
                          sort_order='reverse')
        results = IContentListing(brains)
        return results
