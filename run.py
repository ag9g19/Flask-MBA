from application import init_app

app, app2 = init_app()

if __name__ == "__main__":
    app.run(debug=True)
    app2.run(debug=True)



 




