# Project 3 - Team 3

## Introduction

In this application, users receive SMS alerts for cryptocurrency data that they select.

---

## Set up

Create .env file containing API Key from Coin Market Cap (https://coinmarketcap.com/api/)

The following libraries/imports are used:
* from distutils.log import info
* from requests import Request, Session
* import json
* import time
* import webbrowser
* import pprint
* import os
* from dotenv import load_dotenv
* import pandas as pd
* import questionary
* import smtplib
* from utils import send

---

## Usage

Users are prompted for which crypto currency data they would like to receive and in what converted currency they would like the data to display in. Depending on the movement of the cryptocurrency prices, users will receive data alerts via sms message notifying them of the price changes. User's will also be required to provide phone numbers so as to be able to receive alerts. This is a useful tool for all crypto enthusiasts to consider as it provides real time data from a reliable crypto market pricing data source!

---

## Contributors

Project 3 Team 3 Group Members: Jay Sen, Sim Galbut

---

## License

MIT License

Copyright (c) 2022

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
