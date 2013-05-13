# SciTE Python Extension
# Ben Fisher, 2011

import searchsipmain
import searchutil

def ssip_search_indexed(sModeIn):
    try:
        searchsipmain.searchIndexedMain(sModeIn)
    except searchutil.SipException, ex:
        print 'error:'+str(ex)
    print '>'
        
def ssip_search_unindexed(sRelativeDir):
    try:
        searchsipmain.searchUnindexedMain(sRelativeDir)
    except searchutil.SipException, ex:
        print 'error:'+str(ex)
    print '>'