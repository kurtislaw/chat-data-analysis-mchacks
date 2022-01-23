# Chat analyzer @ McHacks9

![app](https://i.imgur.com/FyMnHLr.png)
[Live Demo](https://mcchat9.herokuapp.com/) | [Github](https://github.com/kurtislaw/mchack-chats)
## ✨ Inspiration
We spend a signifcant amount of our time texting on Instagram. Ever wondered about your texting habits and patterns? Well, we did, that's why we made this program.

Eventually, we decided it would be funnier if we roast you guys, so we gave the app a bit more attitude.
## 🦾 What it does
![individual](https://i.imgur.com/tc6bfRO.png)
It takes a Instagram export, and presents it with its data analyzed. This comes in the form of graphs, numbers and sentence highlights.

## 🚀 Features
![features](https://i.imgur.com/HGi5jJj.png)
### Statistical analysis
- Total messages sent
- Days since the first conversation
- Most popular words/emojis
- Number of conversations held
### Trends spotting
- Response time distribution
- Emotional score per day
- Popular hours distribution
- Chatting frequency over time graph
## 🕵️‍♂️ How we built it
Frontend:
- Bootstrap 5
- HTML, CSS, Javascript

Backend:
- Flask
- pandas
- plotly
- NLTK

Web:
- Heroku

## 🔨 How to use
![dwnld](https://i.imgur.com/WGjoKTS.png)
1. [Download](https://www.instagram.com/download/request/) your Instagram data. Make sure to request it in JSON format!
2. Once you have the zip downloaded, extract and locate the `inbox` folder.
```
EXTRACTED-FOLDER
    |_ messages
        |_ inbox
```
3. [Compress](https://support.microsoft.com/en-us/windows/zip-and-unzip-files-8d28fa72-f2f9-712f-67df-f80cf89fd4e5) this folder ino a zip file. 
4. Decide on whether you want to use the [live demo](https://mcchat9.herokuapp.com/) or build locally. We understand that there are privacy concerns with such intimate information, so we fully support building this project locally!

### Using the [live demo](https://mcchat9.herokuapp.com/)
1. Upload the inbox.zip on the front page.
2. Wait a bit for the process to load. We need to add a progress bar :(
3. That's it!

### Building locally (MacOS only for now)
1. Open terminal and `cd` into the directory `mchack-chats`
2. Type the following into console (make sure you are on the `mchacks-chats` directory)
```zsh
$ export FLASK_APP=chatapp
$ flask run
```
3. Go to `http://127.0.0.1:5000/` on your browser.
## 🤬 Challenges we ran into
1. **Underestimating frontend.**
We do not have experience with front-end development, so trying to learn the basics of web design in a short amount of time was very challenging. 

2. **Time management.**
A lot of the packages we are using are also new to us, such as Flask and plotly. It took a lot of time to read their respective documentations first before we could use the libraries to create our vision.

3. **Over-ambition.**
We had grand visions of rolling animations and custom interactive graphs and even custom scrappers to receive Instagram data. However, parts of the original plan fell short because of the immense time crunch and our obvious lack of experience in some of the areas.
## 🎆 Accomplishments that we're proud of
We are proud that we were overall committed and disciplined over the period of the hackatohn. We got functional graphs out and managed to scale a script into a webapp. This took a lot of extra research outside of what we are taught in school, at least only after our first semester in CS.
## 👩‍🏫 What we learned
The biggest takeaway is that we can actually still function with 2 hours of sleep?? But in terms of technical knowledge, we definitely learnt to not leave frontend till last minute. We all assumed that the data manipulation will take the longest and hence spent the most amount of time on it. However, at the end of the day, it doesn't matter how well a product functions if no one wants to look at it in the first place. 

## 🤓 What's next
Time to find a front-end centric teammate bro.

Features to improve
- beautify frontend
- more graphs
- progress bar
- more spice and attitude in data presentation (less sterile presentation)