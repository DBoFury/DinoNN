# DinoNN

![Project Image](https://user-images.githubusercontent.com/1499751/115730861-549a9600-a38f-11eb-957b-fddc06129a6e.gif)

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [License](#license)
- [Author Info](#author-info)

---

## Description

This project server as a demonstration of my coding skills. I had an idea of making simulation of evolution process, but making computer learn just image classification would not be as excited as making it to learn to play Dino game. I wanted it to be able to play actual game in the browser, not a custom self-made game copy.

To make a decision whether to jump or run, it takes the screenshot, crop it, applies a couple of converts on it and gives it to pre trained Neural Network.

It learns the patterns by looking on premade pictures and setting score to each NN from the population, then it takes best from them and creates a new population based on weights of an old one, and mutates them a bit, and does it all over again. After a couple of epochs, when you satisfied with results of current NN, you stop the training and then you free to use that NN to make if play Dino game.

Project is provided with pre trained model witch you could you right now to make it play Dino game.

#### Technologies

- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115736045-a513f280-a393-11eb-8dbd-ebd3eda15841.png"/> Python
- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115736683-23709480-a394-11eb-83ff-2b9934000eff.png"/> PIL (Python Imaging Library)

- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115754477-e4970a80-a3a4-11eb-8efc-bec67719eff5.png"/> Pandas
- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115737285-ab569e80-a394-11eb-9062-153f7b713199.png"/> Numpy
- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115737361-bc9fab00-a394-11eb-96eb-c5e9b3b81373.png"/> Tensorflow
- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115737402-c6291300-a394-11eb-9151-95412013d4bc.png"/> Selenium
- <img align="left" width="30px" src="https://user-images.githubusercontent.com/1499751/115737432-cc1ef400-a394-11eb-8086-3cfa9419d018.png"/> Pynput

[Back To The Top](#read-me-template)

---

## How To Use

#### Installation

To start using that project on your machine, you need to have a Python 3.7+, download the repository and run command below to install all required dependencies to then use it.

>pip install -r requirements.txt

Run SimulateRun.py and watch it plays.

---

## License

MIT License

Copyright (c) 2021 Didechkin Oleg

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

[Back To The Top](#read-me-template)

---

## Author Info

- Upwork - [Didechkin Oleg](https://www.upwork.com/freelancers/~01bc2c6d8b19205903)
- Fiverr - [Didechkin Oleg](https://www.fiverr.com/dbofury)

[Back To The Top](#read-me-template)
