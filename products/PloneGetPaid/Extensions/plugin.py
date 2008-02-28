

def install_ups( self ):
    from getpaid.ups import plugin
    plugin.UPSPlugin( self ).install()
    return "installed ups"