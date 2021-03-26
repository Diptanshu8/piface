# Raspberry Pi's Piface
A front-end to all my Raspberry Pi hosted services' status and toggle switches to enable/disable them in directly via the browser.

# Installation
1. Fork/Clone this repository.
2. `pip install requirements.txt` to install all dependent modules ( preferable way would be to do it inside a virtualenv).
3. python3 piface.py

# Usage
Once a server has been hosted as per steps mentioned above, you could access the server from browser at the following address:
`http://<server-IP address>:5000`

# Development
To add more features/buttons, follow the following procedure:
1. Add a callback in `routes.py` and attach a route to the callback.
2. Add a button in `main.js` `button_list` and specify the button parameters as follows:
    | Property      | Description |
    | -----------   | ----------- |
    | id            | Unique ID for every button. This ID would be associated with the HTML `button` element. NOTE: id should be unique.|
    | route         | Route in routes.py which would be called when a click event is triggered on this button.                          |
    | redirect      | Port to which redirect has to be done after button click (assuming the redirected server is hosted on Pi.         |
    | show          | Must be set to `true` for the button to be visible.                                                               |
3. Headover to `http://<server-IP address>:5000` and you are good to go!

## Note:
1. Compatible with python3
2. Recommeneded to use virtualenv
