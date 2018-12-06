# LSD_project

### [**Backlog**](https://github.com/Skiparin/LSD_project/projects/1)

### **Tools**
- Database: Postgress
- API: Flask
- Programming Language: Python3
- OS: Linux
- Test: Unittest & Selenium
- Development method: Scrum

### **Functional requirements**
- As a user I want to register an account, so I can log in to my account.
- As a user I want to log in, so I can post stories and write comments.
- As a user I want to post stories, so I can share it.
- As a user I want to comment on posts, so I can share my thoughts.
- As a user I want to upvote so I can share my opinion.
- As a user I want to downvote so I can share my opinion.
- As a user I want to reply on comments, so I can discuss related topics.
- As a user I want to have a collection of points, so I can keep track of my reliability.
- As a user I want to flag content for spam, so I can keep the topics relevant.

### **Non-functional requirements**
- The application should be operating atleast 95% of the time.
- While the application is under maintenance, there should be a mechanism buffering incoming content.


## **Info for the operators**
You can create an issue on the repository if you have any questions, or other inquiries.

Alternatively you can write to any of the following emails:

og1806x9@hotmail.com

2750daugbjerg@gmail.com

n_r_mikkelsen@hotmail.com

tass2012@gmail.com

tvh_1994@hotmail.dk


Sign up for the server:
 - Send a mail to og1806x9@hotmail.com with your public ssh key (each member of the group has to send a key).
 - A member of our group will then grant you non sudo access to the server.

How to access log files:
 - open a terminal and type: ``ssh guest@159.65.116.24``
 - now you are on the server, go to LSD_project: ``cd LSD_project``
 - here you can see the logfile.log

API's to call:

http://159.65.116.24/home

http://159.65.116.24/project_status

http://159.65.116.24/posts

### SLA

- 95% uptime on server.
- 3 seconds response time. (30-50 posts at max)
- 5% or less data loss.

### Grafana

http://159.65.116.24:3000

Username: guest

Password: 1234

Permissions: View Only.
