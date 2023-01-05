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
def basic_wordle():
    
    #Initialise error string for printing error if needed
    errors = ""
    
    #Initialise list for checking input
    accepted_inputs=["Green","G","Orange","O","Red","R","Grey"]
    
    #If using post method (which we are when submitting inputs via a form)
    if request.method == "POST":
        
        #Initialise colour variables
        colour1 = None
        colour2 = None
        colour3 = None
        colour4 = None
        colour5 = None
        
        #Get inputs
        colour1 = request.form["colour1input"]
        colour2 = request.form["colour2input"]
        colour3 = request.form["colour3input"]
        colour4 = request.form["colour4input"]
        colour5 = request.form["colour5input"]
        
        #Check that variables are accepted
        check=accepted_inputs.count(colour1)+accepted_inputs.count(colour2)+accepted_inputs.count(colour3)+accepted_inputs.count(colour4)+accepted_inputs.count(colour5)
        
        #If one or more variables are not accepted, output error
        if check!=5:
            errors += "<p>At least one input is not accepted. Try again.</p>\n"
        
        #Else, complete calculation
        elif check==5:
            
            #Calculate result
            result = print_two_inputs(colour1, colour2)
            
            #Output result as updated HTML page 
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
                <p>Enter your colours:</p>
                <form method="post" action=".">
                    <p><input name="colour1input" /></p>
                    <p><input name="colour2input" /></p>
                    <p><input name="colour3input" /></p>
                    <p><input name="colour4input" /></p>
                    <p><input name="colour5input" /></p>
                    <p><input type="submit" value="Get next Wordle guess" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

if __name__ == '__main__':
  app.run()