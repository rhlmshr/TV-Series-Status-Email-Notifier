# TV-Series-Status-Email-Notifier
This project was created for the [Hacker Camp 2018](https://www.innovaccer.com/hackercamp) organised by Innovaccer. The task description for the following can be found [here](https://www.innovaccer.com/media/hackercamp/SDE-Intern-Assignment.pdf).

## Getting Started
This project demonstrates on finding the release date and status of any TV series. For this I have used an open API known as [TV Maze](https://www.tvmaze.com/api). 

### Build with
* Python3
* SQLiteDb
* Rest Api

## Configuration
Put your Email credentials in the script before getting started:
```
  #Put your credentials here:
    user = 'abc@xyz.com'
    password = 'abcd@1234'
```
This will be the account which will be used by SMTP for sending TV Series Status Mails to the provided Email in the console on runtime.

## How to work
Put your email address where you want the status info and give the list of names of TV series separated by a comma(,). This will store the information to the SQLite Db in Ram and generate an endpoint for the list provided and construct a email body with info needed. That info will be sent to the Email address provided earlier.

### Running
Sample input:
```
Email Address: 'abc@xyz.in'
TV Series: friends, suits, gotham
```
Mail Format:
```
Tv series name: Suits
Status: The show is running but airing date is not determined

Tv series name: Gotham
Status: The next episode airs on 2019-03-15
```
### Video Demo
You can also watch the live demo [here](https://youtu.be/Umf1EAWUsZA).
