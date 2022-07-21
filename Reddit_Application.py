import redditclass as rc
import requests
import json
import PySimpleGUI as sg
import textwrap
import time
import traceback
import logging
import datetime
import os

CLIENT_ID = 'reddit client id'
SECRET_KEY = 'reddit secret key'
USERNAME = 'reddit username'
PASSWORD = 'reddit password'

reddit = rc.Reddit(CLIENT_ID, SECRET_KEY, USERNAME, PASSWORD)

reddit.connect()
userinfo = reddit.user_information(reddit.headers)
rednotifs = reddit.user_inbox(reddit.headers)
indexnumber = -1

def redditnotifications(rednotifications):
    mdata = rednotifications
    notifications = []
    for i in range(len(mdata)):
        mail_data = mdata[i]
        mytext = f"[Subreddit: {mail_data['subreddit']}] | [Author: {mail_data['author']}]"
        notifications.append(mytext)
    return notifications

file_list_column = [[
            sg.Listbox(
            values=[a for a in redditnotifications(rednotifs)], 
            enable_events=True,
            size=(50,10),
            key="-NOTIFICATIONS-"
            )],]

notification_viewer_column = [[sg.Text('Please select a notification', key='ap', size=(100,None), font=('Any 11'))],
                              [sg.Multiline(size=(100,10), key='textbox')],
                              [sg.Button('Post Reply'), sg.Button('Mark as read')]]


layout = [[
    sg.Column(file_list_column),
    sg.VSeperator(),
    sg.Column(notification_viewer_column),
    ]]

sg.theme('DarkAmber')
window = sg.Window("Reddit Notifications", layout, location=(0,0), resizable=True).Finalize()
#window.Maximize()



while True:

    event, values = window.read()
    if event == "-NOTIFICATIONS-":
        try:
            indexnumber = window[event].get_indexes()[0]
            display_text = f"From: {rednotifs[indexnumber]['author']}\n\n{rednotifs[indexnumber]['message']}"
            window.Element('ap').Update(display_text)
        except Exception as e:
            try:
                with open("error.txt", "a") as myfile:
                    myfile.write(f"=== {datetime.datetime.now()} ===\n")
                    myfile.write(str(e))
                    myfile.write('\n')
                    sg.popup_error(f"Error at {datetime.datetime.now()} \n{str(e)} \n\nYou can find the full error log here:\n{os.path.realpath(myfile.name)}/{myfile.name}")
            except Exception as ee:
                sg.popup_error(f"Attempted to create or access error log but encounter error:\n{str(ee)}\nOriginal Error at {datetime.datetime.now()}\n{str(e)}")

    if event == "Post Reply":
        if indexnumber >= 0:
            parent_id = rednotifs[indexnumber]['id']
            reddit.comment_reply(reddit.headers, parent_id, values['textbox'])
            reddit.mark_read(reddit.headers,rednotifs[indexnumber]['id'])
            window.Element('ap').Update("Replied to comment!")
            window.Element('textbox').Update("")
            indexnumber = -1
            time.sleep(1)
            rednotifs = reddit.user_inbox(reddit.headers)
            window.Element('-NOTIFICATIONS-').Update(values=[a for a in redditnotifications(rednotifs)])
    if event == "Mark as read":
        if indexnumber >= 0:
            reddit.mark_read(reddit.headers,rednotifs[indexnumber]['id'])
            window.Element('ap').Update("Marked as read!")
            indexnumber = -1
            time.sleep(1)
            rednotifs = reddit.user_inbox(reddit.headers)
            window.Element('-NOTIFICATIONS-').Update(values=[a for a in redditnotifications(rednotifs)])
    if event == "Exit" or event == sg.WIN_CLOSED:

        break