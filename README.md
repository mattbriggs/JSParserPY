# JSParserPY

Parser will transform JS into an XML file to use in creating # an JS object reference.

This project never really worked exactly right, but I am placing it here in case someone else finds the failed approach useful somehow.

This application will attempt to identify functions in a JS library and roll them into an XML document that describes the JavaScript file. This tool doesn't use JS introspection. As a result, the approach has several drawbacks. I was able to get constructs out of libraries that not were yielding any information to JSDocs, but this approach is really insensitive to dependencies.

I used the output with an XSLT to create a rough version of a library reference and also a table of functions that I could then use JS to call once the library was loaded.

