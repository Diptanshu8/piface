# piface
A front-end to all my Raspberry Pi hosted services' status

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
2. Add a button in `functions.html` and specify the button ID parameter.
3. Add the button ID of the newly created button in `main.js` as key-value pair with value corresponding to the route created in `routes.py`,
    eg. 
    ```buttons[<button ID>]='<route created>'```
4. Reload and you are good to go!

## Note:
1. Compatible with python3
2. Recommeneded to use virtualenv
