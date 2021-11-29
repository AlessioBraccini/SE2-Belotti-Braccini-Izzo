one sig AppSystem{
users: some User,
externalData: some DataProvider,
forum: one Forum
}

sig string{}

abstract sig User{
userDevice : some SmartDevice,
email: one string,
//password: one string,
//name: one string,
//surname: one string,
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
sig IrrigationSystem extends DataProvider{}
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
sig Report{
author: one Agronomist
}{
all a:Agronomist | this in a.reports iff author=a
}

sig Visit{
date: one Date,
farm: one Farm
}

one sig Forum{
topics: set ForumTopic
}
sig ForumTopic{
name: one string,
creator: one User,
posts: disj some Post
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
score: one Float,
rank: one Int
}{
rank > 0
//is ranking daily or annual? 
score.leftPart >= 0
}

sig Farm{
owner: one Farmer,
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
localizationActive : lone GPS
}
sig GPS{}

sig Float{
    leftPart: one Int,
    rightPart: one Int
}{
rightPart >= 0
}

//-------UTILITIES-----
fun isGreater[f1,f2: Float] : lone Float{
	{f: Float | (f=f1 iff (f1.leftPart > f2.leftPart 
				or (f1.leftPart=f2.leftPart and f1.rightPart > f2.rightPart)))
			or (f=f2 iff (f1.leftPart < f2.leftPart 
				or (f1.leftPart = f2.leftPart and f1.rightPart < f2.rightPart)))}
}

//------usefulPREDICATES---
//pred isGoodFarmer[f: Farmer]{}

//-------FACTS-------
fact emailUniqueness{
	no disj u1,u2: User | u1.email=u2.email
}

fact allFarmerInAppSys{
	all f: Farmer, sys: AppSystem | f in sys.users
}

fact oneAgronomistOneDistrict{
	no disj d1,d2: District | d1.manager=d2.manager
}

fact oneFarmOneFarmer{
	no disj f1, f2: Farmer | f1.userFarm=f2.userFarm
}

fact ownerFarm{
	no disj f1, f2: Farmer | all farm: Farm | farm.owner = f1 and f2.userFarm = farm
}

fact senderOfHelpRequestIsTheFarmer{
	all m: Message | one f: Farmer | (m in f.helpRequests implies m.sender=f)
							and (m in f.helpReplies implies m.receiver=f)
}

fact senderOfHelpReplyIsAgronomist{
	all m: Message | one a: Agronomist | (m in a.helpRequests implies m.receiver=a)
							and (m in a.helpReplies implies m.sender=a)
}

fact farmerSendMessageToAreaAgronomist{
	all f: Farmer, m: Message |  (m in f.helpRequests) 
			implies (m.sender).region = (m.receiver).district
								
}

fact farmerReceiveMessageFromAreaAgronomist{
	all f: Farmer, m: Message | one a: Agronomist | (m in f.helpReplies) 
		iff ((m.sender).district = (m.receiver).region
				and m in a.helpReplies)	
}

fact{
	all m: HelpReply | one a: Agronomist | m.sender=a iff m in a.helpReplies
}

fact{
	all m: HelpRequest | one f: Farmer | m.sender=f iff m in f.helpRequests
}	
	

fact agronomistMustRespond{
	all m: HelpRequest,  a: Agronomist | one f: Farmer, m1: HelpReply | 
		(m1 in (a.helpReplies & f.helpReplies) 
		and m1.sender = m.receiver and m1.receiver = m.sender) 
		implies m in a.helpRequests
}

fact visitOnlyInTheArea{
	all a: Agronomist | no dP: DailyPlan, f: Farm | a.dailyPlan=dP and (f in dP.farmsToVisit)
							and f.region!=a.district
}


fact allVisitOfAgroAreInSameArea{
	no disj v1,v2: Visit | all a: Agronomist | v1 in a.dailyVisits and v2 in a.dailyVisits 
					and v1.farm.region!=v2.farm.region and v1.farm.region!=a.district
}

fact noMoreThanOneVisitToTheSameFarmADay{
	all a: Agronomist, disj v1, v2: Visit | no f1,f2: Farm | v1 in a.dailyVisits and v2 in a.dailyVisits
					and f1=v1.farm and f2=v2.farm and f1=f2
}

fact allFarmsInDPSameArea{
	no disj f1, f2: Farm | all dP: DailyPlan | f1 in dP.farmsToVisit and f2 in dP.farmsToVisit 
								and f1.region!=f2.region
}

fact forumCreatorisFarmer{
	no t: ForumTopic | t.creator not in Farmer
}

//a user can't be registered as different
//fact userCanHaveJustOneRole{
//	all sys: AppSystem | none = ...
//}

// + interaction external data with application

//message: check agronomist.area=farmer.area & 

//+ production cropType is the same of the farm
fact prodCropTypeSameAsFarm{
	all f: Farmer | all prodData: ProductionData | f.productionData=prodData 
							implies prodData.cropType = f.farm.cropType
}

fact newsType{
	all n: News | #n.cropType > 0 or #n.area > 0
}

fact ifNewsRelevantThenShow{
	all n: News, f: Farmer | (f.userFarm.cropType in n.cropType or f.userFarm.region in n.area) 
		iff n in f.relevantNews
}

//+ goal: ranking (precedences on harvested/sown)
fact eachFarmerInRanking{
	all r: FarmerRanking | all f: Farmer | f in r.entries.user
}

fact ranking{
	all disj r: FarmerRanking, e1,e2: RankingEntry |  let max = isGreater[e1.score, e2.score] | 
		e1 in r.entries and e2 in r.entries 
		and ((e1.score = max iff e1.rank < e2.rank)
			or (e2.score = max iff e1.rank > e2.rank)) 
}

//fact rankUniqueness{
//	no e1, e2: RankEntry | all r: FarmerRanking | e1.rank = e2.rank and ({(e1), (e2)} in r
//}


//fact differentFarmerForRankEntries{
//	all r:FarmerRanking | no disj e1,e2: RankingEntry | (e1 in r) and (e2 in r) and e1.user=e2.user
//}

fact allForumTopicInForum{
	all f: Forum, t: ForumTopic | t in f.topics
}

fact forumTopicNameUniqueness{
	no disj t1,t2: ForumTopic | t1.name = t2.name
}

//---------ASSERTIONS AND PREDICATES

//G5. 
fact allSteeringInitiativesAreReceivedByPC{
	all pc: PolicyMaker | all a:Agronomist | a.reports in pc.reports 
}

//G6. Visualize relevant data for the farmer business
assert relevantNewsForFarmer{
	all f: Farmer, n: News | n in f.relevantNews iff ((f.userFarm.cropType in n.cropType)
						or (f.userFarm.region in n.area))
}

//G7. Keep track of the production
//pred farmerCanInsertProdEntry{
//	all f: Farmer | 
//}

//G9. Create and participate in forum discussions
assert createADiscussion{
	all sys: AppSystem | all t: ForumTopic | t in sys.forum.topics implies (t.creator in sys.users)
}

assert joinADiscussion{
	all sys: AppSystem | all t: ForumTopic, p: Post | (t in sys.forum.topics and p in t.posts)
					implies (p.user in sys.users)
}

//G8. Request for help/suggestions
pred requestHelpAndGetResponseP[f: Farmer, hm: HelpRequest, a: Agronomist, hp: HelpReply]{
	(hm in f.helpRequests) implies (hm in a.helpRequests and hp in (f.helpReplies & a.helpReplies)
			and hp.sender = a and hp.sender = hm.receiver 
			and hp.receiver = f and hp.receiver = hm.sender and a.district=f.region)
}

assert requestHelpAndGetResponse{
	all f:Farmer, hm: HelpRequest | one a: Agronomist, hp: HelpReply |
		hm in f.helpRequests iff (hm in a.helpRequests and hp in (f.helpReplies & a.helpReplies)
			and hp.sender = a and hp.sender = hm.receiver 
			and hp.receiver = f and hp.receiver = hm.sender and a.district=f.region)
}

//G10. Receive Requests of help all in one place

//G11. Visualize area statistics


pred show {
#User > 0
#Agronomist > 0
#Farmer > 1
#FarmerRanking > 0
}

//check allSteeringInitiativesAreReceivedByPC for 10
check relevantNewsForFarmer for 10
check createADiscussion for 10
check joinADiscussion for 10
check requestHelpAndGetResponse for 5

run requestHelpAndGetResponseP for 5
run show for 3 but 1 AppSystem


