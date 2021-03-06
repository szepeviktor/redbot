#!/usr/bin/env python

"""
Subrequests to do things like range requests, content negotiation checks,
and validation.

This is the base class for all subrequests.
"""

__author__ = "Mark Nottingham <mnot@mnot.net>"
__copyright__ = """\
Copyright (c) 2008-2013 Mark Nottingham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from redbot.resource.fetch import RedFetcher


class SubRequest(RedFetcher):
    """
    Base class for a subrequest of a "main" HttpResource, made to perform
    additional behavioural tests on the resource.
    """
    def __init__(self, base_resource, name):
        self.base = base_resource
        req_hdrs = self.modify_req_hdrs()
        RedFetcher.__init__(self, 
                            self.base.request.uri, 
                            self.base.request.method, 
                            req_hdrs,
                            self.base.request.payload, 
                            self.base.status_cb, 
                            [], 
                            name
        )
        if self.preflight():
            self.base.subreqs[name] = self
    
    def modify_req_hdrs(self):
        """
        Usually overidden; modifies the request's headers.
        
        Make sure it returns a copy of the orignals, not them.
        """
        return list(self.base.orig_req_hdrs)

    def add_note(self, subject, note, subreq=None, **kw):
        self.base.add_note(subject, note, self.name, **kw)
        
    def check_missing_hdrs(self, hdrs, note, subreq_type):
        """
        See if the listed headers are missing in the subrequest; if so,
        set the specified note.
        """
        missing_hdrs = []
        for hdr in hdrs:
            if self.base.response.parsed_headers.has_key(hdr) \
            and not self.response.parsed_headers.has_key(hdr):
                missing_hdrs.append(hdr)
        if missing_hdrs:
            self.add_note('headers', note,
                missing_hdrs=", ".join(missing_hdrs),
                subreq_type=subreq_type
            )
