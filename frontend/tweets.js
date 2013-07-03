.pragma library

var tweets = new Array();
var unlocalizedTweets = 0;

function addTweet(tweet){
    if(tweet.location == false){
        unlocalizedTweets++;
    }
    return tweets.push(tweet)-1;
}

function getLastTweet(){
    return tweets[tweets.length-1];
}

function getUnlocalizedTweets(){
    var result = new Array();
    for(var i in tweets){
        if(tweets[i].location == false){
            result.push(tweets[i]);
        }
    }
    return result;
}

function getTweetAt(index){
    return tweets[index];
}

function getUnlocalizedTweetNumber(){
    return unlocalizedTweets;
}

function clearAll(){
    tweets = new Array();
    unlocalizedTweets = 0;
}

function getTweetById(id){
    for(var t in tweets){
        if(tweets[t].dbId == id)
            return tweets[t];
    }
    return false;
}
