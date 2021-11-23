open util/ordering[RankingEntry]
open util/ordering[ScoreFloat]
open util/boolean

one sig AppSystem{
users: some User,
externalData: some DataProvider,
forum: one Forum
}

abstract sig User{
userDevice : some SmartDevice,
email: one String
}{
#userDevice > 0
}

sig PolicyMaker extends User{
reports: set Report
}

sig Farmer extends User{
region: one District,
userFarm : one Farm,
productionData: disj set ProductionData,
helpRequests: disj set HelpRequest,
helpReplies: disj set HelpReply,
forumDiscussions: disj set ForumTopic,
relevantNews: disj set News
}{
#helpRequests >= #helpReplies
}

sig Agronomist extends User{
district: one District,
dailyPlan : disj set DailyPlan,
dailyVisits: disj set Visit,
helpRequests: disj set HelpRequest,
helpReplies: disj set HelpReply,
reports: disj set Report
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
}{
#sownQty >= 0
#harvestedQty >= 0
}

sig Crop{}

sig News{
cropType: set Crop,
area: set District
}

sig DailyPlan{
farmsToVisit : disj some Farm,
visitDate : one Date,
insertionDate : one Date
}{
}
sig Report{}

sig Visit{
date: one Date,
farm: one Farm
}

one sig Forum{
topics: set ForumTopic
}
sig ForumTopic{
name: one String,
creator: one User,
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

one sig FarmerRanking{
entries: set RankingEntry
}
sig RankingEntry{
user: one Farmer,
score: one ScoreFloat,
rank: one Int
}{
rank > 0
//is ranking daily or annual? 
}

sig Farm{
owner: one Farm,
position : one Location,
region: one District,
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

sig ScoreFloat{
    leftPart: one Int,
    rightPart: one Int
}{
rightPart >= 0
}

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
							implies (m.sender).region = (m.receiver).district
}

fact farmerReceiveMessageFromAreaAgronomist{
	all f: Farmer | all m:Message | (m in f.helpReplies) implies (m.sender).district = (m.receiver).region
}						


fact visitOnlyInTheArea{
	all a: Agronomist | no dP: DailyPlan, f: Farm | a.dailyPlan=dP and (f in dP.farmsToVisit)
							and f.region!=a.district
}

// + interaction external data with application

//message: check agronomist.area=farmer.area & 

//+ production cropType is the same of the farm (pred/assert)
fact prodCropTypeSameAsFarm{
	all f: Farmer | all prodData: ProductionData | f.productionData=prodData 
							implies prodData.cropType = f.farm.cropType
}
pred xor[x,y: Bool]{
	x!=y
}

//+ goal: ranking (precedences on harvested/sown)
//fact ranking{
//	all r: FarmerRanking | all disj e1,e2: RankingEntry | (e1 in r and e2 in r 
//		and e1.score = higherScore[e1.score, e2.score]) iff e1.rank < e2.rank
//}

//fun higherScore[r:FarmerRanking, x,y: ScoreFloat] : one ScoreFloat{
//	all s: ScoreFloat | s in r and s=x and (x.leftPart > y.leftPart or (x.leftPart=y.leftPart
//		and x.rightPart >= y.rightPart))

//}


//fact differentFarmerForRankEntries{
//	all r:FarmerRanking | no disj e1,e2: RankingEntry | (e1 in r) and (e2 in r) and e1.user=e2.user
//}

//---------ASSERTIONS AND PREDICATES

//G5. 
assert allSteeringInitiativesAreReceivedByPC{
	all pc: PolicyMaker | all a:Agronomist | a.reports in pc.reports 
}

//G6. Visualize relevant data for the farmer business
assert relevantNewsForFarmer{
	all f: Farmer | all n: News | n in f.relevantNews iff ((f.userFarm.cropType in n.cropType)
			or (f.userFarm.region in n.area))
}

//G7. Keep track of the production
//pred farmerCanInsertProdEntry{
//	all f: Farmer | 
//}

//G9. Create and participate in forum discussions
assert createADiscussion{
	all sys: AppSystem | all t: ForumTopic | t in sys.forum.topics iff (t.creator in sys.users)
}

assert joinADiscussion{
	all sys: AppSystem | all t: ForumTopic, p: Post | (t in sys.forum.topics and p in t.posts)
					iff (p.user in sys.users)
}

//G8. Request for help/suggestions
pred requestHelpAndGetResponse[f: Farmer, hm: HelpRequest, a: Agronomist]{
	(hm in f.helpRequests) and (hm in a.helpRequests and a.district=f.region) 
}

check allSteeringInitiativesAreReceivedByPC for 10
check relevantNewsForFarmer for 10
check createADiscussion for 10
check joinADiscussion for 10

run requestHelpAndGetResponse{
#Farmer > 0
#HelpRequest > 0
#Agronomist > 0
}


