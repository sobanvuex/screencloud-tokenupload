URL Token Upload for ScreenCloud
================================

ScreenCloud is an easy to use screenshot sharing tool consisting of a cross-platform client and a sharing website: [http://screencloud.net/](http://screencloud.net/)

The goal of this plugin is store (and process) your screanshots by a private endpoint.

Installation
------------

Install [URL Token Upload][current] zip in **ScreenCloud** > **Preferences** > **Online Services** > **More Services** > **Install from URL**

![](http://i.imgur.com/lQIdGt4.png)

**Note:** If you are using ScreenCloud version 1.2.0 or earlier, please use [screencloud-tokenupload release v1.0.0](https://github.com/RezzedUp/screencloud-tokenupload/releases) This version is written with Python 2, which is no longer compatible with ScreenCloud (since ScreenCloud 1.3.0).

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

Installable Endpoint
--------------------

For a ready-to-use endpoint written in Node.js, use [Screencloud Token Upload Server.](https://github.com/RezzedUp/screencloud-tokenupload-server)

Example Endpoint
----------------

Here is an example ednpoint implementation in PHP

```php
<?php
/**
 * Simple file uplaod script.
 * NO WARRANTY. THIS SCRIPT IS ONLY AN EXAMPLE.
 * INPUT VALIDATION IS MINIMAL. DO NOT USE IN PRODUCTION
 *
 * @copyright 2014 Alex Soban
 * @license   http://opensource.org/licenses/MIT
 * @author    Alex Soban <me@soban.co>
 */

define('TOKEN', '<secure_token>');
define('UPLOADS', __DIR__ . '/uploads/');
define('URL', 'http://www.example.com/uploads/');

function output(array $data = array()) {
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}

// decode JSON post data
$contentType = isset($_SERVER['HTTP_CONTENT_TYPE']) ? $_SERVER['HTTP_CONTENT_TYPE'] : '';
if ('application/json' === substr($contentType, 0, 16)) {
    $data = file_get_contents('php://input');
    $_POST = json_decode($data, true);
}

// `name` check is optional
if (empty($_POST) || !isset($_POST['image']) || !isset($_POST['token']) || !isset($_POST['name'])) {
    output(array('error' => 'Invalid input.'));
}

// `token` verification
if ($_POST['token'] !== TOKEN) {
    output(array('error' => 'Invalid token.'));
}

// get the filename and contents
$filename = trim(preg_replace('/[^\d\w.]+/i', '', $_POST['name']));
$image = base64_decode($_POST['image']);

//  "upload" the file to our uploads directory
if (!file_put_contents(UPLOADS . $filename, $image)) {
    output(array('error' => 'Failed saving file.'));
}

// return file public URL
output(array('href' => URL . $filename));
```

[current]: ../../archive/master.zip

