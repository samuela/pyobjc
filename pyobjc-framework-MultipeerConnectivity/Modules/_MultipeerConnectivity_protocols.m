/*
 * This file is generated by objective.metadata
 *
 * Last update: Tue Dec 30 21:46:16 2014
 */

static void __attribute__((__used__)) use_protocols(void)
{
    PyObject* p;
#if defined(__LP64__) && PyObjC_BUILD_RELEASE >= 1010
    p = PyObjC_IdToPython(@protocol(MCAdvertiserAssistantDelegate)); Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(MCBrowserViewControllerDelegate)); Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(MCNearbyServiceAdvertiserDelegate)); Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(MCNearbyServiceBrowserDelegate)); Py_XDECREF(p);
    p = PyObjC_IdToPython(@protocol(MCSessionDelegate)); Py_XDECREF(p);
#endif /* defined(__LP64__) && PyObjC_BUILD_RELEASE >= 1010 */
}
