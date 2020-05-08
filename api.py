from newshub import create_app, create_api_app


api_app = create_api_app()

if __name__ == '__main__':
	api_app.run(debug=True)
