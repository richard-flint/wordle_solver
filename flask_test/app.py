from flask import Flask, request
from function import add_two_numbers,print_two_inputs

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/addtest')
def web_function():
    z=add_two_numbers(1,2)
    return str(z)

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        number1 = None
        number2 = None
        try:
            number1 = str(request.form["number1"])
        except:
            errors += "<p>{!r} is not a string.</p>\n".format(request.form["number1"])
        try:
            number2 = float(request.form["number2"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        
        if number1 is not None and number2 is not None:
            #result = add_two_numbers(number1, number2)
            result = print_two_inputs(number1, number2)
            return '''
                <html>
                    <body>
                        <p>The result is {result}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)
        
    return '''
        <html>
            <body>
                {errors}
                <p>Enter your numbers:</p>
                <form method="post" action=".">
                    <p><input name="number1" /></p>
                    <p><input name="number2" /></p>
                    <p><input type="submit" value="Do calculation" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

if __name__ == '__main__':
  app.run()