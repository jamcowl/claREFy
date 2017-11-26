from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def main():
	return render_template('index.html')

@app.route('/signUp', methods=['GET','POST'])
def signUp():
	print "\n================================================================\n > Button clicked to submit document!\n================================================================\n"
	docInfo = request.form['inputName']
	print "\n================================================================\n > Got info: "+docInfo+"\n================================================================\n"

	# can't do theses
	#return "Yo dawg, you wrote "+docInfo
	#return render_template('documentInfo.html')

if __name__ == "__main__":
	app.debug = True
	app.run()

