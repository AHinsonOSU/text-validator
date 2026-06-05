# text-validator

To prepare to use this microservice, you'll have to 'pip install -r installs.txt'

Once that happens you'll use 'python text-validator.py'

To call this microservice, simply send a post request to the port, uvicorn automatically chooses port 8000.

If you wish to specify another port, then change the uvicorn init at the bottom of the file to the new port.

The microservice intakes a json object with a string, an array of banned characters, and a boolean on if you want to check for potential injection.

Example call that I'm using:

await axios.post("http://localhost:8000/validate", {
            text: name,
            banned: [],
            check_injection: true
});

In this instance I have no banned characters and I just want to check for potential injections from the name attribute.
