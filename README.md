# Templated Web Kiosk for Home Assistant

## Installation via HACS

For [HACS](https://www.hacs.xyz/) simply add this repo as custom repository of type `integration` and install the component. Then follow the manual installation steps to add the configuration.

## Manual Installation

1. Copy `custom_components/templated_web_kiosk` to your `custom_components` folder
2. Add the following to your `configuration.yaml` to activate the component:
    ```yaml
    templated_web_kiosk:
    ```
3. Create a directory named `templated_web_kiosk` within your `config` folder
3. Restart Home Assistant

By default, we use the `templated_web_kiosk` folder within `config`. You can change that by setting the template directory like this in your `configuration.yaml`:

```yaml
templated_web_kiosk:
    template_dir: /some/path/somewhere/else
```

## Usage

Place any file into the template folder and add Home Assistant templating there. Then you can access this file via `/templated_web_kiosk/<filaneme>` and it will render the templates. The content type will be set automatically.

For example, create a file named `test.html` with the following content:
<pre>
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;body&gt;
    &lt;h1&gt;Home Assistant Templating Demo&lt;/h1&gt;
    &lt;p&gt;
        &lt;strong&gt;Sunrise:&lt;/strong&gt; 
        {{ states('sensor.sun_next_dawn') | as_datetime | as_local }}
    &lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;
</pre>

and then go to `/templated_web_kiosk/test.html` on your Home Assistant to see something like this:

<pre>
<h1>Home Assistant Templating Demo</h1>
<strong>Sunrise:</strong> 2026-02-16 07:18:54+01:00
</pre>

**That's it**

## Good To Know

* Use the [Home Assistant file hosting](https://www.home-assistant.io/integrations/http/#hosting-files) folder `www` to expose static content on `/local/`.
* Use the `/local/` URL for static assets that you need, and pass only dynamic content through the templated web kiosk component.
* Templated are loaded on request, so that you can simply change templates without restarting Home Assistant
* There is no authentication, you are responsible for not exposing anything that you don't want exposed. Your Home Assistant is as secure as your templated content.
* We use the Pythong [mimetypes](https://docs.python.org/3/library/mimetypes.html) to determine the content type of the files. If a content type is wrong then you'll need to check how this library determines the content type and add to that.

## Development

This is loosly based on https://aarongodfrey.dev/home%20automation/building_a_home_assistant_custom_component_part_1/ and https://github.com/boralyl/github-custom-component-tutorial but I prefer to use [uv](https://github.com/astral-sh/uv) and to simplify the directory structure.
