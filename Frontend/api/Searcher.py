#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import cgi

print "Content-Type: text/html;charset=utf-8\n"


request = cgi.FieldStorage()
searchRequest = request["searchquery"].value




print 