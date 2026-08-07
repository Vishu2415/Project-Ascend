## Principle 1

Every dependency must have a clear purpose.

Never install a package without understanding why it is needed.

## For Run this 

uvicorn app.main:app --reload

# uvicorn
# FastAPI ko run karne wala ASGI server.

# app.main
# app folder ke andar main.py file.

# :app
# main.py ke andar FastAPI object ka naam.

# --reload
# Code change hote hi server automatically restart ho jata hai.
# Sirf development ke liye use karte hain.