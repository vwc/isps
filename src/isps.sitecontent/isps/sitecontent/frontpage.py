from five import grok
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from plone.app.layout.navigation.interfaces import INavigationRoot

from isps.sitecontent.banner import IBanner


class FrontpageView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('frontpage-view')

    def update(self):
        self.has_banners = len(self.banners()) > 0

    def banners(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IBanner.__identifier__,
                          sort_on='getObjPositionInParent',
                          review_state='published',)
        return results
