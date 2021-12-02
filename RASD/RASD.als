one sig AppSystem{
users: some User,
externalData: some DataProvider,
forum: one Forum,
farmerRanking: one FarmerRanking
}{
	all r: FarmerRanking | r = farmerRanking
}

sig string{}
sig Email{}

abstract sig User{
userDevice : some SmartDevice,
email: one Email,
//password: one string,
//name: one string,
//surname: one string,
}{
#userDevice > 0
}

sig PolicyMaker extends User{
reports: set Report,
statisticData: set DataProvider
}

sig Farmer extends User{
region: one District,
userFarm : one Farm,
productionData: disj set ProductionData,
helpRequests: disj set HelpRequest,
helpReplies: disj set HelpReply,
forumDiscussions: disj set ForumTopic,
relevantNews: disj set News,
weatherForecast: set WeatherForecast
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

sig Farm{
owner: one Farmer,
position : one Location,
cropType: one Crop
}

abstract sig DataProvider{
dateOfMeasure: one Date,
location: one Location
}
sig SoilSensor extends DataProvider{}
sig IrrigationSystem extends DataProvider{}
sig WeatherForecast extends DataProvider{}

sig ProductionData{
farm: one Farm,
sownQty: one Int,
harvestedQty: one Int,
cropType: one Crop,
date: one Date
}{
harvestedQty >= 0
sownQty > 0
}

sig Crop{}

//set of farms that the Agronomist plan to visit for the date visitDate
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

//visits actually done by an Agronomist: can be the same foreseen by the dailyPlan or not
//because an Agronomist can make deviations on his/her dailyPlan (new farms, skipping farm, etc.)
sig Visit{
date: one Date,
farm: one Farm
}

one sig Forum{
topics: set ForumTopic
}
sig ForumTopic{
name: one string,
creator: one Farmer,
posts: disj some Post
}
sig Post{
user: one Farmer,
date: one Date
}

sig News{
cropType: set Crop,
area: set District
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
score.leftPart >= 0
}

//Geographical location (coordinates)
sig Location{
region: one District
}
//Political location
sig District{
manager: one Agronomist
}

sig Date{}

sig SmartDevice{
//localizationActive : lone GPS
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

//-------FACTS-------

//Since email will be the username to access the profile, email must be unique
fact emailUniqueness{
	no disj u1,u2: User | u1.email=u2.email
}

//A device cannot be owned by different users
fact deviceUniqueness{
	all disj u1,u2: User | all d: SmartDevice | d in u1.userDevice implies d not in u2.userDevice
}

fact allUserInAppSys{
	all u: User, sys: AppSystem | u in sys.users
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

fact ownerOfProductionData{
	all p: ProductionData | one f: Farm, u: Farmer | 
		p.farm = f and f.owner = u iff p in u.productionData
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

fact planToVisitOnlyInTheArea{
	all a: Agronomist | no dP: DailyPlan, f: Farm | a.dailyPlan=dP and (f in dP.farmsToVisit)
							and f.region!=a.district
}

fact allVisitedFarmsAreInAgroDistrict{
	all v: Visit | one a: Agronomist | v in a.dailyVisits and v.farm.position.region = a.district
}

fact allDailyPlansAreFromAgronomist{
	all d: DailyPlan | one a:Agronomist | d in a.dailyPlan 
}

//An Agronomist cannot plan two different daily plan for the same day
fact noDifferentDailyPlansWithSameVisitDate{
	all a: Agronomist | no disj dp1, dp2: DailyPlan | (dp1 + dp2) in a.dailyPlan
		and dp1.visitDate = dp2.visitDate
}


fact allVisitOfAgroAreInSameArea{
	no disj v1,v2: Visit | all a: Agronomist | v1 in a.dailyVisits and v2 in a.dailyVisits 
					and v1.farm.location.region!=v2.farm.location.region 
					and v1.farm.location.region!=a.district
}

//All the farms planned by an Agronomist in his/her daily plan must be 
//in the area of competence of Agronomist
fact allPlannedFarmInAgroArea{
	all f: Farm | all dP: DailyPlan, a: Agronomist | dP in a.dailyPlan and f in dP.farmsToVisit
		implies f.position.region = a.district
}

//An agronomist cannot visit the same farm more than once a day
fact noMoreThanOneVisitToTheSameFarmADay{
	all a: Agronomist, disj v1, v2: Visit | no f: Farm | v1 in a.dailyVisits and v2 in a.dailyVisits
					and f=v1.farm and f=v2.farm
}

//All the farms planned in a dailyPlan must be in the same Telangana's district
fact allFarmsInDpSameArea{
	no disj f1, f2: Farm | all dP: DailyPlan | f1 in dP.farmsToVisit and f2 in dP.farmsToVisit 
								and f1.region!=f2.region
}

//Interaction between external data and the application
fact allExternalDataInSys{
	all d: DataProvider | one s: AppSystem | d in s.externalData
}

//production cropType is the same of the farm
fact prodCropTypeSameAsFarm{
	all f: Farmer | all prodData: ProductionData | f.productionData=prodData 
							implies prodData.cropType = f.farm.cropType
}

//a news must have at least one of the two: a concerned cropType or a concerned area
fact newsType{
	all n: News | #n.cropType > 0 or #n.area > 0
}

//all relevant news to the farmer (same CropType or same Area) must be shown to him/her
fact ifNewsRelevantThenShow{
	all n: News, f: Farmer | (f.userFarm.cropType in n.cropType 
			or f.userFarm.position.region in n.area) 
		iff n in f.relevantNews
}

//Ranking (precedences on harvested/sown)
fact eachFarmerInRanking{
	all r: FarmerRanking | all f: Farmer | f in r.entries.user
}

fact ranking{
	all disj r: FarmerRanking, e1,e2: RankingEntry |  let max = isGreater[e1.score, e2.score] | 
		e1 in r.entries and e2 in r.entries 
		and ((e1.score = max iff e1.rank < e2.rank)
			or (e2.score = max iff e1.rank > e2.rank)) 
}


//Topics in Forum and discussions
fact allForumTopicInForum{
	all f: Forum, t: ForumTopic | t in f.topics
}


//If a farmer is posting on a discussion, then he/she's joining it
fact ifFarmerPostThenJoinDiscussion{
	all p: Post, t: ForumTopic | p in t.posts iff t in p.user.forumDiscussions
}

fact topicCreatorsAlsoJoinDiscussion{
	all t: ForumTopic | t in t.creator.forumDiscussions
}

fact forumTopicNameUniqueness{
	no disj t1,t2: ForumTopic | t1.name = t2.name
}


//External data facts
fact weatherRelevantToFarmer{
	all f: Farmer | one w: WeatherForecast | w in f.weatherForecast iff w.location.region = f.region
}

fact locationUniquenessForSoilData{
	no disj d1, d2: SoilSensor | d1.location = d2.location and d1.dateOfMeasure = d2.dateOfMeasure 
}

fact locationUniquenessForWaterData{
	no disj d1, d2: IrrigationSystem | d1.location = d2.location and d1.dateOfMeasure = d2.dateOfMeasure
}

fact locationUniquenessForWeatherForecast{
	no disj d1,d2: WeatherForecast | d1.location = d2.location and d1.dateOfMeasure = d2.dateOfMeasure
}

fact weatherRelevantForFarmer{
	all u: Farmer, w: WeatherForecast | w in u.weatherForecast iff w.location = u.userFarm.position
}

fact locationUniquenessOfFarms{
	no disj f1, f2: Farm | f1.position = f2.position
}

fact justOneAgronomistRelatedToDistrict{
	all d: District | no disj a1,a2: Agronomist | a1.district = d and a2.district = d
}

//---------ASSERTIONS & PREDICATES--------

//G3. Visualize the results of steering initiatives
fact allSteeringInitiativesAreReceivedByPC{
	all pc: PolicyMaker, r: Report | r in pc.reports
}

//G4. Visualize relevant data for the farmer business
assert relevantNewsForFarmer{
	all f: Farmer, n: News | n in f.relevantNews iff ((f.userFarm.cropType in n.cropType)
						or (f.userFarm.position.region in n.area))
}

//G5. Keep track of the production
pred farmerProdEntryInsertion[f: Farmer, p1,p2: ProductionData]{
	p1.cropType = f.userFarm.cropType and p2.cropType = f.userFarm.cropType
	and p1.farm = f.userFarm and p2.farm = f.userFarm
	and (p1.sownQty >= 0 or p1.harvestedQty >= 0) 
	and (p2.harvestedQty >0 or p2.sownQty > 0) and p1!=p2 and p1.date!=p2.date
	and (p1 + p2) in f.productionData
}

//G7. Create and participate in forum discussions
assert createADiscussion{
	all sys: AppSystem | all t: ForumTopic | t in sys.forum.topics implies (t.creator in sys.users)
}

assert joinADiscussion{
	all sys: AppSystem | all t: ForumTopic, p: Post | (t in sys.forum.topics and p in t.posts)
					implies (p.user in sys.users)
}

//G6. Request for help/suggestions
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

//G8. Receive Requests of help all in one place
assert eachHelpRequestDoneIsInAgronomistInbox{
	all hr: HelpRequest | one a: Agronomist | hr in a.helpRequests and hr.sender.region=a.district
}

//G10. Easy daily planning procedure
pred insertDailyPlans[a: Agronomist, dp1,dp2: DailyPlan]{
	(dp1 + dp2) in a.dailyPlan and dp1!=dp2 and #dp1.farmsToVisit > 0 
	and #dp2.farmsToVisit > 0 	
}

assert allFarmsInDailyPlanAreVisitableByAgro{
	all a: Agronomist | all f: Farm, dp: DailyPlan |
		(dp in a.dailyPlan and f in dp.farmsToVisit) implies f.position.region = a.district
}


//-----------RUN & CHECK -------
pred show {
#Agronomist > 0
#Farmer > 1
#RankingEntry > 2
}

//check allSteeringInitiativesAreReceivedByPC for 10
check relevantNewsForFarmer for 10
check createADiscussion for 10
check joinADiscussion for 10
check requestHelpAndGetResponse for 5
check eachHelpRequestDoneIsInAgronomistInbox for 10
check allFarmsInDailyPlanAreVisitableByAgro for 10

run requestHelpAndGetResponseP for 5
run farmerProdEntryInsertion for 5
run show for 3 but 1 AppSystem

run show{
#ForumTopic > 1
#Farmer > 1
#Post > 1
}

run show{
#Report > 2
}


