from cement.core.foundation import CementApp

with CementApp('helloworld') as app:
    app.run()
    print('Hello World')
