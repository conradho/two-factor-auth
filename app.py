"""
hit the first link and then use google authenticator (phone app) to scan it
hit the second link to see the tokens displayed in sync

reference:
    https://github.com/jpf/Twilio-TFA/blob/master/totp_auth.py
    https://github.com/google/google-authenticator/wiki/Key-Uri-Format
    https://github.com/Bouke/django-two-factor-auth/blob/master/two_factor/views/core.py

"""
from flask import Flask, Response

import StringIO
import qrcode

from topt_auth import TotpAuth


app = Flask(__name__)


@app.route('/get_qrcode')
def get_qrcode():
    # the uri you want to give google authenticator
    tfa_uri = 'otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example'
    # the image the end user will scan using google authenticator
    img = qrcode.make(tfa_uri)

    stream = StringIO.StringIO()
    img.save(stream)
    return Response(stream.getvalue(), mimetype='image/png')

@app.route('/token')
def token():
    # sample page to return the current token
    alice = TotpAuth(secret='JBSWY3DPEHPK3PXP')
    return Response(str(alice.generate_token()))



if __name__ == '__main__':
    app.debug = True
    app.run()
