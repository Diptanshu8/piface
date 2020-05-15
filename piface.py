from app import app
if __name__ == '__main__':
    app.config(config.Config)
    print(app.config)
    app.run(debug=True, host='0.0.0.0')
