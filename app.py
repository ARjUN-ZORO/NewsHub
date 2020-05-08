from newshub import create_app, create_api_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
api_app = create_api_app()
app = create_app()


application = DispatcherMiddleware(app,{'/api':api_app})
if __name__ == '__main__':
	run_simple(hostname='127.0.0.1',
        port=5000,application=application,use_reloader=True, use_debugger=True,use_evalex=True)
	# app.run(debug=True, port=8080)
# 	# api_app.run(debug=True)
# 	application.
