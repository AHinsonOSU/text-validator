from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

#
# These are characters that can be used maliciously
# Adapted from: https://www.geeksforgeeks.org/python/sets-in-python/
#
INJECTION_CHARS = set([
    "'", '"', ";", "--", "/*", "*/",
    "|", "&", "$", ">", "<", "\\",
    "{", "}", "(", ")", "=", "#"
])

#
# Request model class
# https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/
#
class ValidationRequest(BaseModel):
    text: str
    banned: list[str] = []
    check_injection: bool = False

#
# Name: decode_ascii_escapes
# Inputs: String
# Outputs: decoded ASCII escapes
#
def decode_ascii_escapes(s: str) -> str:
    return bytes(s, "utf-8").decode("unicode_escape")

@app.post("/validate")
def validate(req: ValidationRequest):
    failed_rules = []

    #
    # Make all text utf-8 and check for ASCII
    #
    normalized = decode_ascii_escapes(req.text)

    # 
    # First, check for any banned characters
    #
    if any(c in normalized for c in req.banned):
        failed_rules.append("banned_characters")

    #
    # Then, check for any characters common in injection attacks
    #
    if req.check_injection:
        if any(c in normalized for c in INJECTION_CHARS):
            failed_rules.append("injection")

    #
    # Return an object that holds the true/false value of the checks
    # and will send what checks may have failed.
    #
    return {
        "valid": len(failed_rules) == 0,
        "failed_rules": failed_rules
    }

#
# Handle the uvicorn calls in the code itself.
#
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
