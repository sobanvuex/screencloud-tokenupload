URL Token Upload for ScreenCloud
================================

ScreenCloud is an easy to use screenshot sharing tool consisting of a cross-platform client and a sharing website: [http://screencloud.net/](http://screencloud.net/)

The goal of this plugin is store (and process) your screanshots by a private endpoint.

Installation
------------

Install [URL Token Upload][current] zip in **ScreenCloud** > **Preferences** > **Online Services** > **More Services** > **Install from URL**

Plugin Configuration
--------------------

The plugin has a few simple configuration options

 * `Token` - Parameter used to authenticate with your endpoint
 * `Address` - URL address of your endpoint
 * `Name` - Name format for your screenshots


Endpoint Configuration
----------------------

For your endpoint to interact properly with this plugin it requires the following functionality:
 * Accept `Content-Type: application/json` over `POST` request method
 * Return JSON formatted response
    * For success: `{"href": "http://example.com/<screenshot>"}`
    * For error: `{"error": "<Error> happened"}`

[current]: ../archive/master.zip
