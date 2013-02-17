django-zcapi
============

A zero-config API for Django projects

This is a quick way of getting a server-side API up and running. I use it when 
starting a Backbone or Angular project, to quickly get a server up and running 
without having to write a ton of code.

This isn't intended for production use (as it exposes your entire
database), you'll want to check out 
[tastypie](http://github.com/toastdriven/django-tastypie) at some point.

Installation
------------

Run the following command from the command prompt:

    python setup.py install

Add zcapi to your installed apps in settings.py:

    INSTALLED_APPS = (
        # Snip
        'zcapi',
    )

Include the zcapi URLs in urls.py:

    from django.conf.urls import patterns, include, url
    urlpatterns = patterns('',
        # Snip
        url(r'^api/', include('zcapi.urls')),
    )

Usage
-----

All models in your project will be available through the API.

Send a GET request to myapp/mymodel for a list of all instances,
or to myapp/mymodel/1 for a specific instance (with PK=1 for this example).

Send POST request to the list URL to create an instance, or to a particular
instance's URL to update that instance.

Send DELETE requests to the list URL to delete every instance, or to a 
particular instance's URL to delete that instance.
