from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import Interface
from plone.app.layout.viewlets.interfaces import IPortalHeader
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy


class SiteNavigationViewlet(grok.Viewlet):
    grok.name('isps.sitecontent.SiteNavViewlet')
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalHeader)

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        self.available = self.testIfThemeEnabled()

    def navStrategy(self):
        context = aq_inner(self.context)
        root = getNavigationRoot(context)
        query = {
            'path': root,
            'review_state': 'published',
            'portal_type': ('isps.sitecontent.previewfolder',
                            'isps.sitecontent.contentpage'),
            'sort_order': 'getObjPositionInParent'
        }
        root_obj = context.unrestrictedTraverse(root)
        strategy = DefaultNavtreeStrategy(root_obj)
        strategy.rootPath = '/'.join(root_obj.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        tree = buildFolderTree(root_obj, root_obj, query, strategy=strategy)
        items = []
        for c in tree['children']:
            item = {}
            item['item'] = c['item']
            item['children'] = c.get('children', '')
            item['itemid'] = c['normalized_id']
            item_id = c['normalized_id']
            if item_id == context.getId():
                item['class'] = 'active'
            else:
                item['class'] = ''
            items.append(item)
        return items

    def isActiveItem(self, itemid):
        context = aq_inner(self.context)
        context_id = context.getId()
        if itemid == context_id:
            return 'navitem active'
        else:
            return 'navitem'

    def testIfThemeEnabled(self):
        theme_header = self.request.get('HTTP_X_THEME_ENABLED', 'No info')
        return theme_header
