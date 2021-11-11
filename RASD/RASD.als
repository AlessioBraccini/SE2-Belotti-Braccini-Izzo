abstract sig User{
userDevice : some SmartDevice
}{
#userDevice > 0
}
sig PolicyMaker extends User{}
abstract sig Farmer extends User{
region: one District,
userFarm : one Farm, //RASD: is it true?
productionData: some ProductionData,
helpRequests: some HelpRequest,
replies: some HelpReply,
forumDiscussions: some ForumTopic
}{
#helpRequests >= #replies
}
//sig GoodFarmer extends Farmer{}
//sig BadFarmer extends Farmer{}
sig Agronomist extends User{
region: one District,
dailyPlan : some DailyPlan,
dailyVisits: some Visit,
requests: some HelpRequest{}
}

abstract sig DataProvider{}
sig SoilSensor extends DataProvider{}
sig IrrigationSysten extends DataProvider{}
sig WeatherForecast extends DataProvider{}

sig ProductionData{
sownQty: one Int,
harvestedQty: one Int,
cropType: one Crop,
date: one Date
}

sig Crop{}

sig DailyPlan{
farmsToVisit : some Farm,
visitDate : one Date
}
sig Report{}
sig Visit{
date: one Date,
farm: one Farm
}

sig Forum{
topics: some ForumTopic
}
sig ForumTopic{
posts: some Post
}
sig Post{
user: one Farmer,
date: one Date
}
abstract sig Message{}
sig HelpRequest extends Message{}
sig HelpReply extends Message{}

sig Farm{
position : one Location,
cropType: one Crop
}
sig Location{}

sig District{}
sig Date{}

sig SmartDevice{
localizationActicve : lone GPS
}
sig GPS{}

//-------UTILITIES-----

//------usefulPREDICATES---
pred isGoodFarmer[f: Farmer]{}

//-------FACTS-------
//an agronomist insert a daily plan for each day
fact planningDaily{
all a : Agronomist |
}

//production cropType is the same of the farm

//---------ASSERTIONS AND PREDICATES-----

