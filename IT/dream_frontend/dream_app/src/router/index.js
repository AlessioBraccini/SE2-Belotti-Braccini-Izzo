import { createRouter, createWebHistory } from 'vue-router'
import About from "../views/About.vue"
import NotFound from "@/views/NotFound";
import SignUpForm from "@/views/SignUpForm";
import LoginPage from "@/views/LoginPage";
import PolicyMakerHomepage from "@/views/PolicyMaker/PolicyMakerHomepage";
import AgronomistHomepage from "@/views/Agronomist/AgronomistHomepage";
import HelpRequests from "@/views/Agronomist/HelpRequests";
import DailyPlan from "@/views/Agronomist/DailyPlan";
import WriteReport from "@/views/Agronomist/WriteReport";
import FarmerHome from "@/views/Farmer/FarmerHome";
import RankingView from "@/views/Agronomist/RankingViewAgro";
import WeatherPage from "@/views/Agronomist/WeatherPage";
import SpecificInfo from "@/views/SpecificInfo";
import UpdatePlan from "@/views/Agronomist/UpdatePlan";
import ShowPlan from "@/views/Agronomist/showPlan";
import ReplyRequest from "@/views/Agronomist/ReplyRequest";
import RankingViewPM from "@/views/PolicyMaker/RankingViewPM";
import SensorPage from "@/views/PolicyMaker/SensorPage";
import ViewReport from "@/views/PolicyMaker/ViewReport";
import RawData from "@/views/PolicyMaker/RawData";
import ViewSpecificPlan from "@/views/PolicyMaker/ViewSpecifiPlan";

// Map of the site paths

const routes = [
    {
        path: '/',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/about',
        name: 'About',
        // component: () => import('../views/About.vue')
        component: About
    },
    {
        path: '/signUp',
        name: 'SignUp',
        component: SignUpForm
    },
    {
        path: '/agronomistHome',
        name: 'AgroHome',
        component: AgronomistHomepage
    },
    {
        path: '/policymakerHome',
        name: 'PMHome',
        component: PolicyMakerHomepage
    },
    {
        path: '/farmerHome',
        name: 'FarmerHome',
        component: FarmerHome
    },
    {
        path: '/agronomistHome/helpRequests',
        name: 'HelpRequests',
        component: HelpRequests
    },
    {
        path: '/agronomistHome/helpRequests/replyRequest',
        name: 'ReplyReq',
        component: ReplyRequest
    },
    {
        path: '/agronomistHome/dailyPlan',
        name: 'DailyPlan',
        component: DailyPlan
    },
    {
        path: '/agronomistHome/updatePlan',
        name: 'UpdatePlan',
        component: UpdatePlan
    },
    {
        path: '/agronomistHome/showPlan',
        name: 'ShowPlan',
        component: ShowPlan
    },
    {
        path: '/agronomistHome/showPlan/viewSpecificPlan',
        name: 'ViewSpecPlan',
        component: ViewSpecificPlan
    },
    {
        path: '/agronomistHome/writeReport',
        name: 'WriteReport',
        component: WriteReport
    },
    {
        path: '/agronomistHome/weatherForecast',
        name: 'WeatherAgro',
        component: WeatherPage
    },
    {
        path: '/ranking',
        name: 'RankPage',
        component: RankingView
    },
    {
        path: '/ranking/specificInfo',
        name: 'SpecificInfo',
        component: SpecificInfo
    },
    {
        path: '/rankingPM',
        name: 'RankingPM',
        component: RankingViewPM
    },
    {
        path: '/steeringInitiative',
        name: 'ViewReport',
        component: ViewReport
    },
    {
        path: '/policymakerHome/sensorsData',
        name: 'Sensors',
        component: SensorPage
    },
    {
        path: '/policymakerHome/sensorsData/rawData',
        name: 'RawData',
        component: RawData
    },


    // Catch 404
    {
        path: '/:catchAll(.*)',
        name: 'NotFound',
        component: NotFound
    }
]

// To cycle between farmers specification see this video for the links with the ':'
// https://www.youtube.com/watch?v=juocv4AtrHo&list=PL4cUxeGkcC9hYYGbV60Vq3IXYNfDk8At1&index=9

// Create a navigable history accessible through back and forward in the browser

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router