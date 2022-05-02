import mechanize
import http.cookiejar as cookielib
import os
from dotenv import load_dotenv


config = load_dotenv(".env")

# cria um repositório de cookies
cookies = cookielib.CookieJar()
# inicia um browser
browser = mechanize.Browser()
# aponta para o repositório de cookies
browser.set_cookiejar(cookies)

browser.open('https://github.com/login')

# o formulário de senha é o primeiro
browser.select_form(nr=0)
browser.form['login'] = os.getenv("GITHUB_USER")
browser.form['password'] = os.getenv("GITHUB_PASSWORD")
# submissão dos dados
browser.submit()
