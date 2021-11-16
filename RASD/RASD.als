sig AppSystem{
users: some User,
externalData: some DataProvider
}

abstract sig User{
userDevice : some SmartDevice,
email: one String
}{
#userDevice > 0
}
sig PolicyMaker extends User{}
sig Farmer extends User{
region: one District,
userFarm : one Farm, //RASD: is it true?
productionData: set ProductionData,
helpRequests: set HelpRequest,
helpReplies: set HelpReply,
forumDiscussions: set ForumTopic
}{
#helpRequests >= #helpReplies
}

sig Agronomist extends User{
region: one District,
dailyPlan : set DailyPlan,
dailyVisits: set Visit,
helpRequests: set HelpRequest,
helpReplies: set HelpReply
}{
#helpRequests >= #helpReplies
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
topics: set ForumTopic
}
sig ForumTopic{
posts: some Post
}
sig Post{
user: one Farmer,
date: one Date
}
abstract sig Message{}
sig HelpRequest extends Message{
sender: one Farmer,
receiver: one Agronomist
}
sig HelpReply extends Message{
sender: one Agronomist,
receiver: one Farmer
}

sig Farm{
position : one Location,
cropType: one Crop
}
sig Location{}

sig District{
manager: one Agronomist
}
sig Date{}

sig SmartDevice{
localizationActicve : lone GPS
}
sig GPS{}

//-------UTILITIES-----

//------usefulPREDICATES---
//pred isGoodFarmer[f: Farmer]{}

//-------FACTS-------
fact oneRegistrationInOneRoleForEachUser{
	all disj u1, u2: User | u1.email=u2.email
}

fact oneAgronomistOneDistrict{
	all disj d1,d2: District | d1.manager!=d2.manager
}

fact senderIsTheFarmer{
	all f: Farmer | no m: Message | ((m in f.helpRequests) and m.sender!=f) 
							or ((m in f.helpReplies) and m.receiver=f)
}

fact senderIsAgronomist{
	all a: Agronomist | no m: Message | a.helpRequests=m and m.receiver!=a
							or a.helpReplies=m and m.sender!=a
}

fact farmerSendMessageToAreaAgronomist{
	all f: Farmer | all m: Message | (m in f.helpRequests)
							implies (m.sender).region = (m.receiver).region
}

fact farmerReceiveMessageFromAreaAgronomist{
	all f: Farmer | all m:Message | (m in f.helpReplies) implies (m.sender).region = (m.receiver).region
}						


// +an agronomist insert a daily plan from the day before to the same date (pred/assert)
//fact planningDaily{
//all a : Agronomist |
//}

// + interaction external data with application

//message: check agronomist.area=farmer.area & 

//+ production cropType is the same of the farm (pred/assert)

//---------ASSERTIONS AND PREDICATES
