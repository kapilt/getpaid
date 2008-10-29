from Products.Five.viewlet import viewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from getpaid.core import interfaces

class WarehouseInfo( viewlet.ViewletBase ):
    
    template = ViewPageTemplateFile('order-warehouse.pt')
    
    order = 3
    
    def update( self ):
        router = interfaces.IOriginRouter( self.__parent__.context )
        self.contact, self.location = router.getOrigin()

    def render( self ):
        return self.__of__( self.__parent__ ).template()
        
    def show( self, **kw ):
        # for viewlet filtering by order state (finance, fullfillment kw args)
        return True