#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

def build_form(username_error, password_error, verify_error, email_error):
    form = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>AJ Signup</title>
            <style type = "text/css">
                .error {
                    color : red;
                }
            </style>
        </head>

        <body>
            <h1>Signup</h1>
            <form name = "username" method = "post">
                <label>
                    Username:
                    <input type = "text" name = "username" />
                </label>
                <p class="error">""" + username_error + """</p>
            <br>
            <form name = "password" method = "post">
                 <label>
                     Password:
                     <input type = "text" name = "password"/>
                 </label>
                 <p class="error">""" + password_error +"""</p>
            <br>
            <form name = "verify" method = "post" >
                <label>
                    Verify Password:
                    <input type = "text" name = "verify" />
                </label>
                <p class="error">""" + verify_error + """</p>
            <br>
            <form name = "email" method = "post">
                <label>
                    Email (Optional):
                    <input type = "text" name = "email"/>
                </label>
                <p class="error">""" + email_error + """</p>
            <br>
            <form>
                <input type= "submit" value= "submit"/>
            </form>
        </body>
    </html>
    """
    return form


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        content = build_form("", "", "", "")
        self.response.write(content)


    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""


        if not valid_username(username):
            username_error ="That is not a valid username."
            have_error = True

        if not valid_password(password):
            password_error = "That is not a valid password."
            have_error = True

        if password != verify:
            verify_error = "The passwords did not match."
            have_error = True

        if not valid_email(email):
            email_error = "That is not a valid email."
            have_error = True

        if have_error:
            self.response.write(build_form(username_error, password_error,verify_error, email_error))

        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def build_welcome(self, username):
        welcome_msg = "<h1> Welcome, " + username + "</h1>"
        return welcome_msg

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(self.build_welcome(username))
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
