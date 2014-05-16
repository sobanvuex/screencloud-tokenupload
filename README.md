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
