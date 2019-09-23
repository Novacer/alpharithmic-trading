# Alpharithmic Trading
Backtest your trading strategy at a click of a button! How much alpha can you generate?


In case you haven't noticed yet, we are LIVE at http://alpharithmic.herokuapp.com. More exciting features to come!

## Technologies used in this project:
* Python Django REST Framework
  * Zipline Live Trading Engine
  * Django Channels
  * Daphne
  * Asynchronous Server Gateway Interface (ASGI)
  * Redis Job Queue
  * Websockets
  * Numpy
  * Matplotlib
  * Scikit-learn (Machine Learning)
  * Pandas
  * REST API
* Angular 6
  * Angular Material
  * Bootstrap
  * Chartjs
  
  
  ## Introduction
  This web application provides hyper-realistic and interactive 
  simulations for trading algorithms. 
  
  With a philosophy that "seeing is believing", every transaction, calculation,
  and event is logged live as the algorithm runs. This provides a superior
  user experience because the user can literally see the algorithm in action, 
  allowing for a greater understanding of the algorithm's behaviour, strengths,
  and weaknesses.
  
  The main driver behind this magic comes from the [Zipline Live Trading Engine](https://www.zipline.io/)
  developed by [Quantopian](https://www.quantopian.com/), an educational platform for learning quantitative finance.
  Some of the algorithms found on this site are inspired by the research efforts and journals
  shared by the community of Quantopian.
  
  The stock pricing data is sourced from the [Quandl WIKI](https://www.quandl.com/databases/WIKIP) API,
  which is available for free for anyone with a Quandl account.
  
  ## Build Your Own Algorithm
  WIP! [Try out what's working so far!](http://alpharithmic.herokuapp.com/build)
  ![Demo](https://user-images.githubusercontent.com/29148427/65398267-3c622f80-dd84-11e9-8b5a-29dcd799cf18.gif)
  
  
  ## The Three Types of Trading Algorithms
  The example algorithms that can be found on this site are divided into 
  three main categories (or classes).
  
  ### The Naive Class
  The Naive Class of algorithms is a class categorized by the fact
  that they track and trade a single stock using some strategy. You can tell
  if an algorithm falls under the Naive Class if you have to pick a stock to trade
  in the simulation parameters. Conceptually,these are the easiest algorithms to understand. However, simple does not
  mean it's ineffective! There are tons of great strategies that fall under this 
  category. For starters, we recommend checking out the 
  [RSI Divergence Strategy!](http://alpharithmic.herokuapp.com/algorithms/rsi-divergence)
  
  ### The Advanced Class
  The Advanced Class of algorithms differs from the Naive Class in that you do not
  get to pick a stock! Instead, the Advanced Class will scan the market to identify the
  best combination of stocks to long/short in your portfolio to maximize your return.
  These algorithms leverage the Pipeline API provided by Zipline, which provides a series
  of filters and sorts to identify the strongest stocks based on some quantitative factor.
  For a great demonstration of this, try out the 
  [Trend Follower Algorithm!](http://alpharithmic.herokuapp.com/algorithms/trend-follow)
  
  ### The Machine Learning Class
  This is a special class of algorithms that specifically integrate machine learning classifiers and
  capabilities to derive a set of insights that the above two classes cannot. Here's a great example
  using a [Random Forest Regressor Algorithm!](http://alpharithmic.herokuapp.com/algorithms/random-forest-regression)
   
 
 ## Diagrams
 ![alpha arch](https://user-images.githubusercontent.com/29148427/46925503-27204500-cffa-11e8-9c21-550dff245b13.jpg)

